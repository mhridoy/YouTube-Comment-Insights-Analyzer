import os
import json
import time
import logging
from googleapiclient.discovery import build
import traceback

# Initialize logging
logger = logging.getLogger(__name__)

# YouTube API key
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

# Cache directory
CACHE_DIR = '.cache/youtube_comments'
os.makedirs(CACHE_DIR, exist_ok=True)

def get_video_id(url):
    """
    Extracts the video ID from a YouTube URL.
    """
    try:
        if 'youtube.com/watch?v=' in url:
            return url.split('v=')[1].split('&')[0]
        elif 'youtu.be/' in url:
            return url.split('/')[-1]
        else:
            return None
    except Exception as e:
        logger.error(f"Error extracting video ID: {str(e)}")
        return None

def get_cache_file_path(video_id):
    """
    Generates the cache file path for a given video ID.
    """
    return os.path.join(CACHE_DIR, f'{video_id}.json')

def get_cached_comments(video_id):
    """
    Retrieves cached comments for a given video ID if cache is valid (1 hour).
    """
    try:
        cache_file = get_cache_file_path(video_id)
        if os.path.exists(cache_file):
            with open(cache_file, 'r', encoding='utf-8') as f:
                cached_data = json.load(f)
            if time.time() - cached_data['timestamp'] < 3600:  # 1 hour
                logger.info(f"Using cached comments for video ID: {video_id}")
                return cached_data['comments']
    except Exception as e:
        logger.error(f"Error retrieving cached comments: {str(e)}")
    return None

def cache_comments(video_id, comments):
    """
    Caches comments for a given video ID.
    """
    try:
        cache_file = get_cache_file_path(video_id)
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump({'timestamp': time.time(), 'comments': comments}, f)
        logger.info(f"Comments cached for video ID: {video_id}")
    except Exception as e:
        logger.error(f"Error caching comments: {str(e)}")

def get_video_comments(video_url, max_results=500):
    """
    Retrieves comments from a YouTube video given its URL.
    """
    try:
        if not YOUTUBE_API_KEY:
            logger.error("YouTube API key not found.")
            return None

        video_id = get_video_id(video_url)
        if not video_id:
            logger.error("Invalid YouTube URL. Could not extract video ID.")
            return None

        # Check cache
        cached_comments = get_cached_comments(video_id)
        if cached_comments:
            return cached_comments[:max_results]

        # Initialize YouTube API client
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

        comments = []
        next_page_token = None

        while len(comments) < max_results:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                textFormat="plainText",
                maxResults=min(100, max_results - len(comments)),
                pageToken=next_page_token
            )
            response = request.execute()

            for item in response.get("items", []):
                comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                comments.append(comment)

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

        # Cache the comments
        cache_comments(video_id, comments)

        logger.info(f"Fetched {len(comments)} comments for video ID: {video_id}")
        return comments[:max_results]

    except Exception as e:
        logger.error(f"An error occurred while fetching comments: {str(e)}")
        logger.error(traceback.format_exc())
        return None
