import requests

def google():
    res = requests.get("https://www.google.com/")
    print(res.text)
