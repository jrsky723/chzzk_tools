import re
import datetime
from urllib.parse import urlparse

def parse_time(time_str):
    # HH:MM:SS 또는 MM:SS 또는 SS 형식의 문자열을 datetime.timedelta 객체로 변환
    pattern = re.compile(r'^(\d?\d):([0-5]\d):([0-5]\d)$|^([0-5]?\d):([0-5]\d)$')
    if pattern.match(time_str):
        parts = time_str.split(":")
        if len(parts) == 3:
            return datetime.timedelta(hours=int(parts[0]), minutes=int(parts[1]), seconds=int(parts[2]))
        elif len(parts) == 2:
            return datetime.timedelta(minutes=int(parts[0]), seconds=int(parts[1]))
        elif len(parts) == 1:
            return datetime.timedelta(seconds=int(parts[0]))
    else:
        raise ValueError("Invalid time format")
    

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception as e:
        print(f"Error in is_valid_url  {e}")
        return False
    

def hash_to_color(hash_str):
        hex_color = hash_str[2:8]
        return int(hex_color, 16)