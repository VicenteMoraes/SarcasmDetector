import json
import requests
import re
from bs4 import BeautifulSoup


def read_body(text, outlet):
    soup = BeautifulSoup(text, "lxml")
    if outlet == "theonion":
        body = soup.find("meta", attrs={"property": "og:description"})["content"]
    elif outlet == "huffingtonpost":
        body = soup.find_all("div", attrs={"class": "content-list-component text"})
    else:
        body = soup.find_all("p")
    body = re.sub("<(.*?)>", "", str(body))
    body = body.replace('\n', '')
    if outlet != "theonion":
        body = body[1:-1]
    print(body)
    return body


header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}
with open("data.txt", "w") as wf:
    with open("Sarcasm_Headlines_Dataset.json", "r") as rf:
        while True:
            line = rf.readline()
            if not line:
                break
            data = json.loads(line)
            url = data["article_link"]
            if "huffingtonpost" in url:
                outlet = "huffingtonpost"
            elif "theonion" in url:
                outlet = "theonion"
            elif "theguardian" in url:
                url = url.replace("https://www.huffingtonpost.com", "")
                outlet = "theguardian"
            else:
                print("OOPS " + url)
                break
            try:
                request = requests.get(url, headers=header)
            except ConnectionError:
                continue
            body = read_body(request.text, outlet)
            wf.write(body + "\n")
