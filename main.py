from bs4 import BeautifulSoup, Comment
import webbrowser
import win32api
import requests
import json
import time

URL_PATH = "urls.json"
DELAY = 300
MESSAGE = "Change in website detected."

if __name__ == "__main__":
    with open(URL_PATH, "r") as file:
        urls = json.load(file)
    last = {}
    for url in urls.keys():
        last[url] = None

    try:
        while(True):
            for url in urls.keys():
                # Fetch desired text from html document
                r = requests.get(urls[url])
                soup = BeautifulSoup(r.content, "html.parser")

                comments = soup.find_all(text=lambda text: isinstance(text, Comment))
                for comment in comments:
                    comment.extract()

                text = soup.prettify()
                print(text)

                # Check if text has changed
                if (not last[url] == text and not last[url] == None):
                    win32api.MessageBox(0, MESSAGE, "Alert", 0x00001000)
                    webbrowser.open(urls[url], 2)

                    splitA = text.split("\n")
                    splitB = last[url].split("\n")
                    print(set(splitA).symmetric_difference(set(splitB)))
                else:
                    

                    t = time.localtime()
                    cur_time = time.strftime("%H:%M:%S ", t)
                    print(cur_time + "No changes detected")
        
                # Update last text seen
                last[url] = text

            time.sleep(DELAY)

    finally:
        win32api.MessageBox(0, "The script has stopped", "Alert", 0x00001000)