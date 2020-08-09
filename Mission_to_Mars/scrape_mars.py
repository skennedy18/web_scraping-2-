from bs4 import BeautifulSoup
from splinter import Browser
import pymongo
import pandas as pd
import requests
import time

def scrape():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)    
    #News
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(2)
    soup = BeautifulSoup(browser.html, 'html.parser')
    titles = soup.find("ul",class_='item_list')
    newstitle = []
    for ul in titles:
        for a in titles.findAll('a'):
            newstitle.append(a.text)
    news_title = newstitle[1]
    news_paragraph = soup.find("div", class_="article_teaser_body").text
    # print(f'title:{news_title} paragraph:{news_paragraph}')

    #Images
    url_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_image)
    browser.find_by_id('full_image').click()
    featured_image_url = browser.find_by_css('.fancybox-image').first['src']
    # featured_image_url

    #Weather
    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)
    time.sleep(2)
    soup = BeautifulSoup(browser.html,"html.parser")
    article = soup.findAll('article')
    weather = article[1].findAll('span', class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")[4].text

    #Facts
    url_facts = "https://space-facts.com/mars/"
    df_facts = pd.read_html(url_facts)[0]
    df_facts.columns = ["Facts","Values"]
    clean_table = df_facts.set_index(["Facts"])
    mars_table = clean_table.to_html()
    facts = mars_table.replace("\n", "")

    #Hemis
    url_hemi = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemi)
    time.sleep(3)
    soup3 = BeautifulSoup(browser.html, 'html.parser')
    results = soup3.find('div', class_='collapsible results')
    hemis=results.find_all('a')
    hemis_urls=[]
    for hemi in hemis:
        if hemi.h3:
            title = hemi.h3.text
            next_ = hemi["href"]
            browser.visit("https://astrogeology.usgs.gov/" + next_)
            time.sleep(3)
            soup = BeautifulSoup(browser.html, 'html.parser')
            hemisphere2 = soup.find("div",class_= "downloads")
            img=hemisphere2.ul.a["href"]
            hemisphere_dict={}
            hemisphere_dict['title']=title
            hemisphere_dict["image_url"]=img
            hemis_urls.append(hemisphere_dict)
    
    browser.quit()
    
    #returning
    mars={
    "news_title": news_title,
    "news_paragraph": news_paragraph,
    "featured_image_url": featured_image_url,
    "weather": weather,
    "facts": facts,
    "hemi_urls": hemis_urls
    }
    return mars