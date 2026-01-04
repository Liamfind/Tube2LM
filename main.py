"""
AI 工具包 - 主入口文件
"""
from modules.youtube.scraper import YouTubeScraper
from core.logger import setup_logger

# ==================== 配置区域 ====================
# 在这里填入你要抓取的 YouTube 频道 URL
CHANNEL_URL = "https://www.youtube.com/@thefutur/videos"  # The Futur 频道

# 排重文件（可选）：如果提供了已抓取的 Excel 文件路径，将自动排除这些视频
EXCLUDE_FILE = None  # 例如："/path/to/existing_videos.xlsx" 或 None
# ==================================================

logger = setup_logger("main")


def main():
    """主函数"""
    logger.info("=" * 60)
    logger.info("YouTube 视频 URL 抓取工具")
    logger.info("=" * 60)
    
    # 检查是否配置了频道 URL
    if "example" in CHANNEL_URL or not CHANNEL_URL:
        logger.error("请先在 main.py 中配置 CHANNEL_URL 变量！")
        logger.info("示例：CHANNEL_URL = 'https://www.youtube.com/@channelname/videos'")
        return
    
    try:
        # 创建抓取器实例
        scraper = YouTubeScraper()
        
        # 抓取视频 URL 和发布时间
        logger.info("开始抓取视频链接和发布时间...")
        if EXCLUDE_FILE:
            logger.info(f"使用排重文件：{EXCLUDE_FILE}")
        video_data = scraper.scrape_channel(
            CHANNEL_URL, 
            include_date=True,
            exclude_file=EXCLUDE_FILE
        )
        
        if not video_data:
            logger.warning("未抓取到任何视频链接，请检查频道 URL 是否正确")
            return
        
        # 保存到文件（Excel 格式，包含发布时间）
        output_file = scraper.save_urls(video_data, channel_url=CHANNEL_URL, file_format='excel')
        
        logger.info("=" * 60)
        logger.info(f"抓取完成！共抓取 {len(video_data)} 条视频链接")
        logger.info(f"结果已保存到：{output_file}")
        logger.info("文件格式：Excel（包含 URL、发布时间、视频ID）")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"程序执行失败：{str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    main()

