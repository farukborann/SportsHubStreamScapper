from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import json
import time
import googleAuth

site_url = "https://sportshub.stream/soccer-live-streamz/"
blog_url = "https://tht-ideathi.blogspot.com/"

leagues = ["Portugal. League Cup"] # "Colombia. Primera A"  

def getBlogId(token):
    url = "https://www.googleapis.com/blogger/v3/blogs/byurl?&url=" + blog_url
    header = {'Authorization': 'Bearer ' + token}
    blog_info_req = requests.get(url, headers=header)
    return json.loads(blog_info_req.text)['id']


def addPostToBlog(token, blog_id, title, content):
    url = "https://www.googleapis.com/blogger/v3/blogs/" + blog_id + "/posts/"
    data = json.dumps({
        "kind": "blogger#post",
        "blog": {
            "id": blog_id
        },
        "title": title,
        "content": content
    })
    header = {'Authorization': 'Bearer ' + token}
    request = requests.post(url, data, headers=header)
    print("Added => " + title)
    # print(request.text)
    # print('________________________________________________')
    time.sleep(0.5)


def main():
    token = googleAuth.main()
    blog_id = getBlogId(token)

    options = Options()
    # options.add_argument("disable-gpu")
    # options.add_argument("--headless")
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    options.add_argument("window-size=1920,1080")
    driver = webdriver.Chrome(service=Service("./chromedriver.exe"), options=options)

    try:
        driver.get(site_url)
        WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.CLASS_NAME, "list-events")))
    except Exception:
        print("Site can't Loaded !!!")
        driver.quit()

    html = driver.page_source
    driver.quit()

    site = BeautifulSoup(html, "html.parser")
    match_items = site.find_all('li', class_='wrap-events-item')

    for match in match_items:
        desc = match.find('span', class_='evdesc event-desc').find('span').text.strip()
        for league in leagues:
            if(desc.startswith(league)):
                title = match.find('span', class_='mr-5').text.strip()
                url = urljoin(site_url, match.find('a', class_='item-event d-block').get('href'))
                addPostToBlog(token, blog_id, title, content=desc + "\n" + url)
                break

main()





























#Hello, I will not show the code to secure my labor.
#Thank you for your understanding.
#Since the blog page I set up is new, my api limits do not allow me to share more than 5 posts in a minute.
#For this reason, only the "Portugal. League Cup" category football matches.
#Thanks for watching.