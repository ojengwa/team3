from celery import Celery
import requests

def url_ok(url):
    r = requests.head(url)
    if r.status_code == 200:
    	return True
    else:
    	return False
    	
print url_ok('https://api.github.com/events')