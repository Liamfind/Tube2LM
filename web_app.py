"""
YouTube 视频 URL 抓取工具 - Web 界面
在浏览器中打开 http://localhost:5000 即可使用
"""
from flask import Flask, render_template, request, jsonify, send_file
import os
import uuid
import threading
from pathlib import Path
from werkzeug.utils import secure_filename
from modules.youtube.scraper import YouTubeScraper
from core.logger import setup_logger
from core.config import OUTPUT_DIR

BASE_DIR = Path(__file__).parent

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 限制上传文件大小为 16MB
app.config['UPLOAD_FOLDER'] = BASE_DIR / 'uploads'
app.config['UPLOAD_FOLDER'].mkdir(exist_ok=True)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # 禁用静态文件缓存

logger = setup_logger("web_app")

ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

# 全局进度存储（任务ID -> 进度信息）
progress_store = {}
progress_lock = threading.Lock()


@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def update_progress(task_id, stage, progress, message, current_count=0, total_count=0, estimated_time=None):
    """更新进度信息"""
    with progress_lock:
        progress_store[task_id] = {
            'stage': stage,
            'progress': progress,
            'message': message,
            'current_count': current_count,
            'total_count': total_count,
            'estimated_time': estimated_time
        }
    # 添加调试日志（每10%或重要阶段记录）
    if progress % 10 == 0 or stage in ['init', 'starting', 'completed', 'error']:
        logger.info(f"进度更新 [任务 {task_id[:8]}...]: {stage} {progress}% - {message}")


@app.route('/api/scrape', methods=['POST'])
def scrape():
    """抓取视频 URL 的 API 接口（支持文件上传排重和进度跟踪）"""
    task_id = str(uuid.uuid4())
    
    try:
        # 初始化进度
        update_progress(task_id, 'init', 0, '正在初始化...', 0, 0)
        
        # 检查是否有文件上传
        exclude_file_path = None
        if 'exclude_file' in request.files:
            file = request.files['exclude_file']
            if file and file.filename and allowed_file(file.filename):
                update_progress(task_id, 'reading_exclude', 2, '正在读取排重文件...', 0, 0)
                filename = secure_filename(file.filename)
                filepath = app.config['UPLOAD_FOLDER'] / filename
                file.save(filepath)
                exclude_file_path = str(filepath)
                logger.info(f"已上传排重文件：{filename}")
                update_progress(task_id, 'reading_exclude', 5, f'已读取排重文件：{filename}', 0, 0)
        
        # 获取频道 URL（支持 JSON 和表单数据）
        if request.is_json:
            data = request.json
            channel_url = data.get('channel_url', '').strip()
            include_date = data.get('include_date', True)
        else:
            channel_url = request.form.get('channel_url', '').strip()
            include_date = request.form.get('include_date', 'true').lower() == 'true'
        
        if not channel_url:
            with progress_lock:
                if task_id in progress_store:
                    del progress_store[task_id]
            return jsonify({
                'success': False,
                'error': '请提供频道 URL'
            }), 400
        
        logger.info(f"收到抓取请求：{channel_url}")
        if exclude_file_path:
            logger.info(f"使用排重文件：{exclude_file_path}")
        
        # 创建进度回调函数
        def progress_callback(stage, progress, message, current_count=0, total_count=0, estimated_time=None):
            update_progress(task_id, stage, progress, message, current_count, total_count, estimated_time)
        
        # 创建抓取器并执行抓取（在后台线程中执行）
        def scrape_task():
            try:
                # 确保任务ID在进度存储中
                update_progress(task_id, 'starting', 1, '正在启动抓取任务...', 0, 0)
                
                scraper = YouTubeScraper()
                video_data = scraper.scrape_channel(
                    channel_url, 
                    include_date=include_date,
                    exclude_file=exclude_file_path,
                    progress_callback=progress_callback
                )
                
                if not video_data:
                    update_progress(task_id, 'error', 0, '未抓取到任何视频链接', 0, 0)
                    return
                
                # 保存到文件（Excel 格式）
                update_progress(task_id, 'saving', 90, '正在保存文件...', len(video_data), len(video_data))
                output_file = scraper.save_urls(
                    video_data, 
                    channel_url=channel_url, 
                    file_format='excel'
                )
                
                # 返回结果，包含实际抓取数量
                actual_count = len(video_data)
                logger.info(f"抓取完成，实际数量：{actual_count} 条")
                
                # 清理上传的临时文件
                if exclude_file_path and Path(exclude_file_path).exists():
                    try:
                        Path(exclude_file_path).unlink()
                    except:
                        pass
                
                # 更新最终进度
                update_progress(task_id, 'completed', 100, '抓取完成！', actual_count, actual_count, 0)
                
                # 保存结果到进度中
                with progress_lock:
                    if task_id in progress_store:
                        progress_store[task_id]['result'] = {
                            'success': True,
                            'count': actual_count,
                            'target_min': 200,
                            'target_max': 300,
                            'filename': output_file.name,
                            'filepath': str(output_file),
                            'urls': [item.get('url', '') if isinstance(item, dict) else item for item in video_data[:10]]
                        }
            except Exception as e:
                logger.error(f"抓取失败：{str(e)}", exc_info=True)
                update_progress(task_id, 'error', 0, f'抓取失败：{str(e)}', 0, 0)
                with progress_lock:
                    if task_id in progress_store:
                        progress_store[task_id]['result'] = {
                            'success': False,
                            'error': str(e)
                        }
        
        # 在后台线程中执行抓取任务
        thread = threading.Thread(target=scrape_task)
        thread.daemon = True
        thread.start()
        
        # 立即返回任务ID
        return jsonify({
            'success': True,
            'task_id': task_id
        })
        
    except Exception as e:
        logger.error(f"创建抓取任务失败：{str(e)}", exc_info=True)
        with progress_lock:
            if task_id in progress_store:
                del progress_store[task_id]
        return jsonify({
            'success': False,
            'error': f'创建抓取任务失败：{str(e)}'
        }), 500


@app.route('/api/progress/<task_id>')
def get_progress(task_id):
    """获取抓取进度"""
    with progress_lock:
        if task_id not in progress_store:
            return jsonify({
                'success': False,
                'error': '任务不存在或已过期'
            }), 404
        
        progress_info = progress_store[task_id].copy()
        
        # 如果任务完成或出错，返回结果并清理
        if progress_info.get('stage') in ['completed', 'error']:
            result = progress_info.get('result')
            # 延迟清理，给前端一些时间获取结果
            return jsonify({
                'success': True,
                **progress_info,
                'result': result
            })
        
        return jsonify({
            'success': True,
            **progress_info
        })


@app.route('/api/download/<filename>')
def download(filename):
    """下载结果文件"""
    try:
        filepath = OUTPUT_DIR / filename
        if filepath.exists():
            return send_file(
                filepath,
                as_attachment=True,
                download_name=filename,
                mimetype='text/plain'
            )
        else:
            return jsonify({'error': '文件不存在'}), 404
    except Exception as e:
        logger.error(f"下载失败：{str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/files')
def list_files():
    """列出所有输出文件"""
    try:
        files = []
        for file in sorted(OUTPUT_DIR.glob('urls_snapshot_*.txt'), reverse=True):
            files.append({
                'name': file.name,
                'size': file.stat().st_size,
                'modified': file.stat().st_mtime
            })
        return jsonify({'files': files})
    except Exception as e:
        logger.error(f"列出文件失败：{str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # 确保模板目录存在
    template_dir = Path(__file__).parent / 'templates'
    template_dir.mkdir(exist_ok=True)
    
    # 支持环境变量 PORT（用于云部署，如 Railway, Render）
    PORT = int(os.environ.get('PORT', 8080))
    # 支持环境变量 HOST（用于云部署）
    HOST = os.environ.get('HOST', '127.0.0.1')
    
    # 如果是云部署（PORT 由环境变量设置），使用 0.0.0.0
    if os.environ.get('PORT'):
        HOST = '0.0.0.0'
    
    print("=" * 60)
    print("YouTube 视频 URL 抓取工具 - Web 界面")
    print("=" * 60)
    print("正在启动服务器...")
    
    if HOST == '0.0.0.0':
        print(f"服务器地址：http://0.0.0.0:{PORT}")
        print("（云部署模式，请使用云服务提供的 URL）")
    else:
        print(f"请在浏览器中打开：http://127.0.0.1:{PORT}")
        print(f"或：http://localhost:{PORT}")
    
    print("按 Ctrl+C 停止服务器")
    print("=" * 60)
    
    try:
        app.run(debug=False, host=HOST, port=PORT, use_reloader=False)
        print("\n✅ 服务器已启动")
        if HOST != '0.0.0.0':
            print(f"请在浏览器中打开：http://127.0.0.1:{PORT}")
            print(f"或：http://localhost:{PORT}")
        print("按 Ctrl+C 停止服务器")
    except OSError as e:
        if "Address already in use" in str(e):
            PORT = 5002
            print(f"\n⚠️  端口 {PORT} 被占用，尝试使用端口 {PORT}...")
            app.run(debug=False, host=HOST, port=PORT, use_reloader=False)
            print(f"\n✅ 服务器已启动（使用端口 {PORT}）")
            if HOST != '0.0.0.0':
                print(f"请在浏览器中打开：http://127.0.0.1:{PORT}")
                print(f"或：http://localhost:{PORT}")
            print("按 Ctrl+C 停止服务器")
        else:
            raise

