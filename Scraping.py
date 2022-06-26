import wikipediaapi
import requests
import csv
import pandas as pd
import xlsxwriter
from urllib.request import urlopen, Request
from urllib.parse import urlencode, urlunparse
from bs4 import BeautifulSoup

wiki_wiki = wikipediaapi.Wikipedia('en')
phrase = input("Input Phrase Here ")
page =  wiki_wiki.page(phrase)
print("Page - Exists: %s" % page.exists())

# Get URL, Title, Name, Creation Date from Wikipedia

data_wikipedia = []
response = requests.get(page.fullurl)
soup = BeautifulSoup(response.content, 'html.parser')
Wikipedia_Name = soup.find(id="firstHeading").text #Get Wikipedia Article Name
pageinfo = page.fullurl + "?action=info"
response = requests.get(pageinfo)
soup = BeautifulSoup(response.content, 'html.parser')
first_time = soup.find(id='mw-pageinfo-firsttime').find_all('td')[1] #Get Wikipedia Article Creation Date
data_wikipedia.append([page.fullurl, Wikipedia_Name, page.title, page.summary[0:200], first_time.text])
df1 = pd.DataFrame(data_wikipedia)
df1.columns = ["URL", "Page Name", "Page Title", "Content", "Created at"]

# Get URL, Title, Date Published, and Related Wikipedia Article on Bing Search
url = 'https://www.bing.com/search?q={}'.format(phrase)
req = requests.post(url)
data_bing = []
soup = BeautifulSoup(req.text, 'html.parser')
items = soup.findAll('li', 'b_algo') 
for it in items [0:10]:
    urllink = it.find('a')['href'] #Get 10 URLs
    title = it.find('a', href=True).text #Get 10 Titles
    try : date_published = it.find('span', 'news_dt').text
    except : date_published = '' #Get date published
    data_bing.append([urllink, title, date_published, page.fullurl])
df2 = pd.DataFrame(data_bing)
df2.columns = ["URL", "Title", "Date Published", "Wikipedia"]
with pd.ExcelWriter('results/Scraping.xlsx') as writer:
    df1.to_excel(writer, sheet_name='Sheet_1')
    df2.to_excel(writer, sheet_name='Sheet_2')
    writer.save()

print('done')
