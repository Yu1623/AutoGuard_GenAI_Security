import requests
from bs4 import BeautifulSoup
from selenium import webdriver

url = requests.get("https://www.cdc.gov/autism/site.html")
soup = BeautifulSoup(url.text, 'html.parser')
s = soup.find('div', class_="cdc-dfe-sitemap__pane cdc-dfe-sitemap__pane--gen tab-pane")
urls = []
for link in soup.find_all('a'):
    if 'autism' in link.get('href'):
        if link.get('href') in urls:
            continue
        else:
            urls += [link.get('href')]
print(urls)
"""
url = input("Enter url")
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
doc_content = []
for content in soup.find_all('p'):
    doc_content += [content]
new_doc = []
for content in doc_content:
    content = str(content)
    s = content.split()
    print(s)
    l = []
    for i in s:
        if i != '<p>' or i != '</p>':
            l += [i]
    new_content = " ".join(l)
    new_doc += [new_content]
print(new_doc)
"""

driver = webdriver.Firefox(executable_path = r'/home/yuxuan/Documents/geckodriver-v0.34.0-linux-aarch64/geckodriver')
driver.get("https://www.cdc.gov/health-topics.html")
html = driver.page_source
print(html)
