import requests

def post_information(y):
    res = requests.post('https://httpbin.org/post', data={'st3': 'jim hopper'})