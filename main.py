import requests
from bs4 import BeautifulSoup
import time
import win32api

URL = "https://www.sz.rwth-aachen.de/cms/SZ/Fremdsprachen/Termine/~iphr/Einstufungstests/"
TAG = "p"
CLASS = "update"
DELAY = 1800
MESSAGE = "Change in website detected. Go register."

if __name__ == "__main__":
    last = None
    while(True):
        # Fetch desired text from html document
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, "html.parser")
        text = soup.find(TAG, {"class": CLASS}).text
        
        # Check if text has changed
        if (not last == text and not last == None):
            win32api.MessageBox(0, MESSAGE, "Alert", 0x00001000) 
            break
        else:
            print("No changes detected")
            
        # Update last text seen and wait
        last = text
        time.sleep(DELAY)