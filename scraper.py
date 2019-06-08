import numpy as np
import matplotlib.pyplot as plt
import json
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup


def read_body(text, tag, attr):
    soup = BeautifulSoup(text, "lxml")
    body = soup.find(tag, attrs=attr)
    if tag == "meta":
        body = body["content"]
    body = re.sub("<(.*?)>", "", str(body))
    body = body.replace('\n', '')
    print(body)
    return body


header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

with open("Sarcasm_Headlines_Dataset.json", "r") as rf:
   while True:
       line = rf.readline()
       if not line:
           break
       data = json.loads(line)
       url = data["article_link"]
       if "huffingtonpost" in url:
           tag = "div"
           atrr = {"class": "post-contents yr-entry-text"}
       elif "theonion" in url:
           tag = "meta"
           atrr = {"property": "og:description"}
       elif "theguardian" in url:
           url = url.replace("https://www.huffingtonpost.com", "")
           tag = "div"
           atrr = {"class": "content__article-body from-content-api js-article__body"}
       else:
           print("OOPS " + url)
           break
       try:
           request = requests.get(url, headers=header)
       except ConnectionError:
           continue
       read_body(request.text, tag, atrr)
