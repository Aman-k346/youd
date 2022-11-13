import requests

def check_video_url(video_id):
    checker_url = "https://www.youtube.com/oembed?url="
    video_url = checker_url + video_id

    request = requests.get(video_url)
    if request.status_code == 200:
        return True
    else:
        return False
        