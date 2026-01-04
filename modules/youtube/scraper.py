"""
YouTube 视频 URL 抓取模块
使用 yt-dlp 库抓取指定频道的最新视频链接
"""
import yt_dlp
import pandas as pd
import re
from typing import List, Optional, Set
from pathlib import Path

from core.config import OUTPUT_DIR, YOUTUBE_CONFIG
from core.logger import setup_logger

logger = setup_logger("youtube_scraper")


class YouTubeScraper:
    """YouTube 视频抓取器"""
    
    def __init__(self, max_videos: int = None, min_videos: int = None):
        """
        初始化抓取器
        
        Args:
            max_videos: 最大抓取数量，默认使用配置文件中的值
            min_videos: 最少抓取数量，默认使用配置文件中的值
        """
        self.max_videos = max_videos or YOUTUBE_CONFIG["max_videos"]
        self.min_videos = min_videos or YOUTUBE_CONFIG["min_videos"]
        logger.info(f"初始化 YouTube 抓取器，配置：最多 {self.max_videos} 条，最少 {self.min_videos} 条")
    
    def _get_channel_upload_url(self, channel_url: str) -> str:
        """
        将频道 URL 转换为上传列表 URL
        
        Args:
            channel_url: 频道 URL（支持多种格式）
            
        Returns:
            上传列表 URL
        """
        # 如果已经是上传列表 URL，直接返回
        if "/videos" in channel_url or "/playlists" in channel_url:
            return channel_url
        
        # 如果是频道主页 URL，转换为上传列表
        if "/channel/" in channel_url or "/c/" in channel_url or "/user/" in channel_url or "/@" in channel_url:
            # 确保以 /videos 结尾
            if not channel_url.endswith("/videos"):
                channel_url = channel_url.rstrip("/") + "/videos"
            return channel_url
        
        return channel_url
    
    def _extract_channel_name(self, channel_url: str) -> str:
        """
        从频道 URL 中提取频道名称
        
        Args:
            channel_url: YouTube 频道 URL
            
        Returns:
            频道名称（用于文件命名）
        """
        # 提取 @频道名 格式
        match = re.search(r'@([^/]+)', channel_url)
        if match:
            return match.group(1)
        
        # 提取 /channel/ 或 /c/ 格式
        match = re.search(r'/(?:channel|c|user)/([^/]+)', channel_url)
        if match:
            return match.group(1)
        
        # 如果无法提取，使用默认名称
        return "youtube_channel"
    
    def _extract_video_id_from_url(self, url: str) -> Optional[str]:
        """
        从 YouTube URL 中提取视频 ID
        
        Args:
            url: YouTube 视频 URL
            
        Returns:
            视频 ID，如果无法提取则返回 None
        """
        if not url:
            return None
        
        # 匹配 watch?v=VIDEO_ID 格式
        match = re.search(r'(?:watch\?v=|/)([a-zA-Z0-9_-]{11})', url)
        if match:
            return match.group(1)
        
        return None
    
    def load_existing_videos(self, excel_file_path: str) -> Set[str]:
        """
        从 Excel 文件中加载已存在的视频 ID 列表
        
        Args:
            excel_file_path: Excel 文件路径
            
        Returns:
            视频 ID 集合（用于快速查找）
        """
        existing_ids = set()
        
        try:
            if not Path(excel_file_path).exists():
                logger.warning(f"文件不存在：{excel_file_path}")
                return existing_ids
            
            logger.info(f"正在读取已存在的视频清单：{excel_file_path}")
            
            # 读取 Excel 文件
            df = pd.read_excel(excel_file_path, engine='openpyxl')
            
            # 尝试从不同列中提取视频 ID
            url_column = None
            video_id_column = None
            
            # 查找 URL 列
            for col in df.columns:
                col_lower = str(col).lower()
                if 'url' in col_lower:
                    url_column = col
                    break
            
            # 查找视频ID列
            for col in df.columns:
                col_lower = str(col).lower()
                if 'id' in col_lower or 'video' in col_lower:
                    video_id_column = col
                    break
            
            # 从 URL 列提取视频 ID
            if url_column:
                for url in df[url_column].dropna():
                    video_id = self._extract_video_id_from_url(str(url))
                    if video_id:
                        existing_ids.add(video_id)
            
            # 从视频ID列提取
            if video_id_column:
                for vid_id in df[video_id_column].dropna():
                    vid_id_str = str(vid_id).strip()
                    if len(vid_id_str) == 11:  # YouTube 视频 ID 通常是 11 位
                        existing_ids.add(vid_id_str)
            
            logger.info(f"从 Excel 文件中提取到 {len(existing_ids)} 个已存在的视频 ID")
            
        except Exception as e:
            logger.error(f"读取 Excel 文件失败：{str(e)}", exc_info=True)
            logger.warning("将跳过排重功能，继续正常抓取")
        
        return existing_ids
    
    def scrape_channel(self, channel_url: str, include_date: bool = False, exclude_file: Optional[str] = None, progress_callback=None) -> List[dict]:
        """
        抓取频道视频 URL 列表
        
        Args:
            channel_url: YouTube 频道 URL
            include_date: 是否包含发布时间
            exclude_file: 已存在视频的 Excel 文件路径（用于排重）
            
        Returns:
            视频信息列表（按发布时间从近到远排序）
            格式: [{'url': '...', 'upload_date': '20240101'}, ...] 或 ['url1', 'url2', ...]
        """
        upload_url = self._get_channel_upload_url(channel_url)
        logger.info(f"开始抓取频道：{upload_url}")
        
        # 进度回调函数
        def update_progress(stage, progress, message, current=0, total=0, estimated_time=None):
            if progress_callback:
                try:
                    progress_callback(stage, progress, message, current, total, estimated_time)
                except:
                    pass
        
        # 加载已存在的视频 ID（用于排重）
        existing_video_ids = set()
        if exclude_file:
            update_progress('reading_exclude', 5, '正在读取排重文件...', 0, 0)
            existing_video_ids = self.load_existing_videos(exclude_file)
            if existing_video_ids:
                logger.info(f"已加载 {len(existing_video_ids)} 个已存在的视频，将自动排除")
                update_progress('reading_exclude', 5, f'已读取 {len(existing_video_ids)} 个已存在的视频', 0, 0)
        
        video_urls = []
        video_data = []  # 存储包含日期的完整信息
        
        update_progress('connecting', 10, '正在连接 YouTube 服务器...', 0, 0)
        
        try:
            # 如果需要日期，必须处理每个视频来获取发布时间
            # 注意：这会比只获取URL慢很多，因为需要为每个视频调用API
            if include_date:
                # 优化配置：只使用一个客户端，减少API调用
                ydl_opts_flat = {
                    'extract_flat': False,  # 必须处理每个视频才能获取日期
                    'quiet': False,
                    'no_warnings': False,
                    'ignoreerrors': True,
                    'playlistend': self.max_videos,
                    'playlistreverse': False,
                    'skip_download': True,  # 不下载视频
                    'writesubtitles': False,
                    'writeautomaticsub': False,
                    'writethumbnail': False,
                    'writedescription': False,
                    'writeinfojson': False,
                    'extractor_args': {
                        'youtube': {
                            'player_client': ['android'],  # 只使用一个客户端，减少50%的API调用
                            'player_skip': ['webpage', 'configs', 'iframe'],  # 跳过不必要的解析
                            'skip': ['dash', 'hls'],
                        }
                    }
                }
                logger.info("正在获取频道视频列表（包含发布时间）...")
                logger.info("⚠️  注意：获取发布时间需要处理每个视频，会比只获取URL慢很多")
                logger.info(f"预计需要处理 {min(len(entries) if 'entries' in locals() else self.max_videos, self.max_videos)} 个视频，请耐心等待...")
                process_mode = True  # 必须处理每个视频
            else:
                # 不需要日期时，使用极速模式
                ydl_opts_flat = {
                    'extract_flat': 'in_playlist',  # 在播放列表中只提取元数据，不处理单个视频
                    'quiet': False,
                    'no_warnings': False,
                    'ignoreerrors': True,
                    'playlistend': self.max_videos,  # 限制抓取数量
                    'playlistreverse': False,  # 确保从最新开始（Newest First）
                    'extractor_args': {
                        'youtube': {
                            'player_client': ['android', 'web'],  # 使用移动端和网页端客户端
                            'player_skip': ['webpage', 'configs'],  # 跳过网页和配置解析
                        }
                    }
                }
                logger.info("正在获取频道视频列表（极速模式，避免反爬虫验证）...")
                process_mode = False
            
            update_progress('fetching', 15, '正在获取频道信息...', 0, 0)
            
            # 在长时间操作期间添加心跳更新（让用户知道还在工作）
            import threading
            import time
            heartbeat_active = [True]
            
            def heartbeat():
                """心跳更新，防止用户以为程序卡住了"""
                stages = [
                    '正在连接 YouTube 服务器...',
                    '正在获取频道数据...',
                    '正在解析频道信息...',
                    '正在获取视频列表...',
                ]
                stage_idx = 0
                base_progress = 15  # 基础进度
                max_progress = 25   # 最大进度（在解析完成前）
                
                while heartbeat_active[0]:
                    time.sleep(3)  # 每3秒更新一次
                    if heartbeat_active[0]:
                        # 进度在15-25%之间缓慢递增，不会回退
                        # 每3秒增加约1%，最多到25%
                        current_progress = min(base_progress + stage_idx, max_progress)
                        msg = stages[stage_idx % len(stages)]
                        update_progress('fetching', current_progress, msg, 0, 0)
                        stage_idx += 1
                        # 如果超过最大进度，保持在最大进度，但消息继续循环
                        # 注意：不要重置stage_idx，让它继续增长，这样进度不会回退
            
            heartbeat_thread = threading.Thread(target=heartbeat, daemon=True)
            heartbeat_thread.start()
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts_flat) as ydl:
                    # 如果需要日期，使用 process=True 来获取完整信息
                    # 如果不需要日期，使用 process=False 配合 extract_flat
                    info = ydl.extract_info(upload_url, download=False, process=process_mode)
            finally:
                heartbeat_active[0] = False  # 停止心跳
                
                if not info:
                    logger.error("无法获取频道信息")
                    return []
                
                # 提取视频条目
                entries = info.get('entries', [])
                
                # 如果 entries 是生成器，转换为列表
                if hasattr(entries, '__iter__') and not isinstance(entries, (list, tuple)):
                    logger.info("检测到生成器，正在转换为列表...")
                    update_progress('parsing', 25, '正在解析视频列表...', 0, 0)
                    entries = list(entries)
                
                logger.info(f"获取到 {len(entries)} 个视频条目")
                total_entries = min(len(entries), self.max_videos)
                update_progress('parsing', 30, f'已解析 {total_entries} 个视频条目', 0, total_entries)
                
                # 如果数量不足，尝试重新获取（可能是分页问题）
                if len(entries) < self.min_videos:
                    logger.warning(f"⚠️ 只获取到 {len(entries)} 条（目标：{self.min_videos}-{self.max_videos} 条）")
                    logger.info("尝试使用备用方法重新获取...")
                    
                    # 备用方法：使用不同的配置重新获取
                    ydl_opts_full = {
                        'quiet': False,
                        'no_warnings': False,
                        'ignoreerrors': True,
                        'playlistend': self.max_videos,
                        'playlistreverse': False,
                        'skip_download': True,
                        'writesubtitles': False,
                        'writeautomaticsub': False,
                        'writethumbnail': False,
                        'writedescription': False,
                        'writeinfojson': False,
                        'extract_flat': False,
                        'extractor_args': {
                            'youtube': {
                                'skip': ['dash', 'hls'],
                            }
                        }
                    }
                    
                    with yt_dlp.YoutubeDL(ydl_opts_full) as ydl_full:
                        logger.info("使用备用方法重新获取（可能需要更长时间）...")
                        info_full = ydl_full.extract_info(upload_url, download=False, process=True)
                        
                        if info_full:
                            entries_full = info_full.get('entries', [])
                            if hasattr(entries_full, '__iter__') and not isinstance(entries_full, (list, tuple)):
                                logger.info("正在处理播放列表条目...")
                                entries_full = list(entries_full)
                            
                            if len(entries_full) > len(entries):
                                entries = entries_full
                                logger.info(f"✅ 备用方法获取到 {len(entries)} 个视频条目")
                            else:
                                logger.info(f"备用方法获取到 {len(entries_full)} 个视频条目（与之前相同）")
                
                if not entries:
                    logger.warning("未找到视频条目")
                    return []
                
                # 提取视频 URL 和发布时间
                # YouTube 频道的上传列表默认就是按时间从近到远排序的（Newest First）
                total_to_process = min(len(entries), self.max_videos)
                processed_count = 0
                
                for idx, entry in enumerate(entries, 1):
                    if idx > self.max_videos:
                        break
                    
                    # 跳过 None 条目
                    if entry is None:
                        logger.warning(f"第 {idx} 条视频条目为空，跳过")
                        continue
                    
                    # 更新进度（每处理一个视频）
                    processed_count += 1
                    if include_date:
                        # 如果需要日期，进度从 30% 到 85%
                        progress = 30 + int((processed_count / total_to_process) * 55)
                        stage_msg = '正在提取视频信息和发布时间'
                    else:
                        # 如果不需要日期，进度从 30% 到 85%
                        progress = 30 + int((processed_count / total_to_process) * 55)
                        stage_msg = '正在提取视频链接'
                    
                    # 计算预计剩余时间（基于实际处理速度）
                    estimated_remaining = None
                    if processed_count >= 5:  # 至少处理5个后才估算
                        # 使用实际处理速度估算（如果之前有记录）
                        if not hasattr(update_progress, 'start_time'):
                            import time
                            update_progress.start_time = time.time()
                            update_progress.last_count = 0
                        
                        if processed_count > update_progress.last_count:
                            import time
                            elapsed = time.time() - update_progress.start_time
                            if elapsed > 0:
                                avg_time_per_video = elapsed / processed_count
                                remaining_videos = total_to_process - processed_count
                                estimated_remaining = int(remaining_videos * avg_time_per_video)
                                update_progress.last_count = processed_count
                    
                    # 优先使用 id 字段构建完整 URL
                    video_id = entry.get('id') if entry else None
                    video_url = None
                    
                    if video_id:
                        video_url = f"https://www.youtube.com/watch?v={video_id}"
                    else:
                        # 尝试从 url 字段获取
                        url = entry.get('url')
                        if url:
                            video_url = url
                        else:
                            # 尝试从 webpage_url 获取
                            webpage_url = entry.get('webpage_url')
                            if webpage_url:
                                video_url = webpage_url
                            else:
                                # 尝试从 video_id 字段获取
                                vid_id = entry.get('video_id')
                                if vid_id:
                                    video_url = f"https://www.youtube.com/watch?v={vid_id}"
                    
                    if not video_url:
                        continue
                    
                    # 排重检查：如果视频 ID 已存在，跳过
                    if existing_video_ids and video_id:
                        if video_id in existing_video_ids:
                            logger.debug(f"跳过已存在的视频：{video_id}")
                            continue
                    
                    # 提取发布时间
                    upload_date = None
                    if include_date:
                        # 尝试多种方式获取发布时间
                        # 优先从播放列表元数据中获取（如果可用）
                        upload_date = (
                            entry.get('upload_date') or 
                            entry.get('release_date') or
                            entry.get('timestamp') or
                            entry.get('published') or  # 播放列表可能包含此字段
                            entry.get('published_time') or
                            None
                        )
                        
                        # 如果 upload_date 是时间戳，转换为日期格式
                        if upload_date and isinstance(upload_date, (int, float)):
                            from datetime import datetime
                            try:
                                upload_date = datetime.fromtimestamp(upload_date).strftime('%Y%m%d')
                            except:
                                upload_date = None
                        elif upload_date and isinstance(upload_date, str) and len(upload_date) > 8:
                            # 如果是其他格式，尝试提取日期部分
                            try:
                                from datetime import datetime
                                dt = datetime.fromisoformat(upload_date.replace('Z', '+00:00'))
                                upload_date = dt.strftime('%Y%m%d')
                            except:
                                upload_date = upload_date[:8] if len(upload_date) >= 8 else upload_date
                        
                    
                    # 保存数据（这里才是真正"已抓取"的数量）
                    if include_date:
                        video_data.append({
                            'url': video_url,
                            'upload_date': upload_date or 'N/A',
                            'video_id': video_id or entry.get('video_id', 'N/A')
                        })
                        actual_saved = len(video_data)  # 实际保存的数量
                    else:
                        video_urls.append(video_url)
                        actual_saved = len(video_urls)
                    
                    # 每5个视频更新一次进度（更频繁的更新，让用户看到进度）
                    # 使用实际保存的数量，而不是处理的数量
                    if actual_saved % 5 == 0 or actual_saved == total_to_process or actual_saved <= 10:
                        update_progress(
                            'extracting',
                            progress,
                            f'{stage_msg}... (已抓取 {actual_saved}/{total_to_process})',
                            actual_saved,  # 使用实际保存的数量
                            total_to_process,
                            estimated_remaining
                        )
                    
                    # 每 50 条输出一次日志
                    if idx % 50 == 0:
                        logger.info(f"已处理 {idx}/{min(len(entries), self.max_videos)} 条视频链接...")
                
                result_count = len(video_data) if include_date else len(video_urls)
                update_progress('extracting', 85, f'已完成提取，共 {result_count} 条视频', result_count, result_count)
                
                # 如果有排重，显示排重信息
                if existing_video_ids:
                    excluded_count = sum(1 for e in entries[:self.max_videos] if e and e.get('id') in existing_video_ids)
                    logger.info(f"成功抓取 {result_count} 条视频链接（已排除 {excluded_count} 条已存在的视频）")
                else:
                    logger.info(f"成功抓取 {result_count} 条视频链接")
                
                # 检查是否满足最少数量要求
                if result_count < self.min_videos:
                    logger.warning(
                        f"⚠️ 抓取到的视频数量 ({result_count}) 少于最少要求 ({self.min_videos})"
                    )
                    logger.info("可能的原因：")
                    logger.info("  1. 频道实际视频数量少于预期")
                    logger.info("  2. YouTube 访问限制")
                    logger.info("  3. 频道有部分视频为私有或已删除")
                else:
                    logger.info(f"✅ 成功抓取 {result_count} 条视频链接（目标：{self.min_videos}-{self.max_videos} 条）")
                
        except Exception as e:
            logger.error(f"抓取过程中发生错误：{str(e)}", exc_info=True)
            raise
        
        return video_data if include_date else video_urls
    
    def save_urls(self, video_data, filename: Optional[str] = None, channel_url: Optional[str] = None, file_format: str = 'excel') -> Path:
        """
        保存视频 URL 列表到文件（支持 Excel 和 TXT 格式）
        
        Args:
            video_data: 视频数据（可以是 URL 字符串列表或包含 URL 和日期的字典列表）
            filename: 文件名，如果为 None 则自动生成（使用频道名称）
            channel_url: 频道 URL（用于提取频道名称）
            file_format: 保存格式，'excel' 或 'txt'，默认为 'excel'
            
        Returns:
            保存的文件路径
        """
        from datetime import datetime
        import pandas as pd
        
        # 提取频道名称用于文件命名
        channel_name = "youtube_channel"
        if channel_url:
            channel_name = self._extract_channel_name(channel_url)
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            if file_format == 'excel':
                filename = f"{channel_name}_{timestamp}.xlsx"
            else:
                filename = f"{channel_name}_{timestamp}.txt"
        
        filepath = OUTPUT_DIR / filename
        
        # 判断数据格式并准备数据
        if video_data and isinstance(video_data[0], dict):
            # 包含日期的格式
            data_list = []
            for item in video_data:
                data_list.append({
                    'URL': item.get('url', ''),
                    '发布时间': item.get('upload_date', 'N/A'),
                    '视频ID': item.get('video_id', 'N/A')
                })
            
            df = pd.DataFrame(data_list)
            
            if file_format == 'excel':
                # 保存为 Excel 格式
                df.to_excel(filepath, index=False, engine='openpyxl')
                logger.info(f"已保存 {len(video_data)} 条数据到 Excel 文件：{filepath}")
            else:
                # 保存为 TXT 格式（制表符分隔）
                df.to_csv(filepath, sep='\t', index=False, encoding='utf-8')
                logger.info(f"已保存 {len(video_data)} 条数据到文本文件：{filepath}")
        else:
            # 纯 URL 格式
            if file_format == 'excel':
                df = pd.DataFrame({'URL': video_data})
                df.to_excel(filepath, index=False, engine='openpyxl')
                logger.info(f"已保存 {len(video_data)} 条 URL 到 Excel 文件：{filepath}")
            else:
                with open(filepath, 'w', encoding='utf-8') as f:
                    for url in video_data:
                        f.write(url + '\n')
                logger.info(f"已保存 {len(video_data)} 条 URL 到文本文件：{filepath}")
        
        return filepath

