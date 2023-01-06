import asyncio
import re
from concurrent.futures import ProcessPoolExecutor
#from concurrent.futures import ThreadPoolExecutor
from yt_dlp import YoutubeDL as YDL
from configs.constants import YOUTUBE_COOKIE_FILE

PPE = ProcessPoolExecutor()
#TPE = ThreadPoolExecutor()

class NoLoggerOutputs:
    def error(msg):
      pass
    def warning(msg):
      pass
    def debug(msg):
      pass

def extract_livestream_info(channel_url: str, logger=NoLoggerOutputs) -> dict:
  """
    Get information on a single youtube livestream synchronously.
  """
  try:
    with YDL({"quiet": True,
              "cookiefile": YOUTUBE_COOKIE_FILE,
              "logger": logger}) as ydl:
      info = ydl.extract_info(f"{channel_url}/live", download=False)
      return {"success": True,
              "original_url":channel_url,
              "name": info["channel"],
              "title": info["title"],
              "description": info["description"],
              "thumbnail": info["thumbnail"],
              "url": info["webpage_url"],
              "is_live": info["is_live"],
              "release_timestamp": info["release_timestamp"]}
  except:
    return {"success": False,
            "original_url":channel_url}

async def extract_livestream_infos(*channel_urls, loop=None) -> dict:
  """
    Get information on multiple youtube livestreams asynchronously.
    Returns empty list if none are live.
  """
  loop = loop or asyncio.get_event_loop()
  futs = [loop.run_in_executor(
          PPE, extract_livestream_info, channel_url) 
          for channel_url in channel_urls]
  infos = await asyncio.gather(*futs)
  return list(filter(lambda x: 'success' in x and x['success']==True, infos))

def is_youtube_link(url:str) -> bool:
  """
    Checks if your url is a YouTube link.
  """
  _regex = (
      r'(https?://)?(www\.)?'
      '(youtube|youtu|youtube-nocookie)\.(com|be)/'
      '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
  matches = re.findall(_regex, url)
  if matches is not None and len(matches) == 1:
      return True
  return False

async def get_audio_info(url:str, logger=NoLoggerOutputs) -> dict:
  """
   Get information on a specific YouTube video's audio formats.
  """
  try:
    with YDL({"quiet": True,
              'format': 'bestaudio',
              "cookiefile": YOUTUBE_COOKIE_FILE,
              'logger': logger}) as ydl:
      info = ydl.extract_info(url, download=False)
      return {
        'success' : True,
        'info' : info
      }
  except Exception as e:
    return {
      'success' : False,
      'error' : str(e)
    }

async def get_audio_search_results(search:str, logger=NoLoggerOutputs) -> dict:
  """
   Get information on videos's audio formats resulting from specific query.
  """
  try:
    with YDL({"quiet": True,
              'format': 'bestaudio',
              "cookiefile": YOUTUBE_COOKIE_FILE,
              'logger': logger}) as ydl:
      search_results = ydl.extract_info(f'ytsearch:"{search}"', download=False)
      return {
        'success' : True,
        'search_results' : search_results
      }
  except Exception as e:
    return {
      'success' : False,
      'error' : str(e)
    }

def get_query_type(query:str):
  """
  Tells you what type of query has been given:
  Types:
    * youtube_url
    * non_youtube_url
    * youtube_search
  """
  if is_youtube_link(query):
    return "youtube_url"
  
  if query.startswith('http'):
    return "non_youtube_url"

  return "youtube_search"
