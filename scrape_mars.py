from bs4 import BeautifulSoup
import requests
import os
from splinter import Browser
import time
import pandas as pd

def scrape():
    executable_path = {'executable_path': 'c:/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    
    # Title and paragraph
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    
    soup = BeautifulSoup(browser.html, 'html.parser')
    
    title = soup.find("div", class_="content_title").text
    paragraph_text = soup.find("div", class_="rollover_description_inner").text
    
    # Latest Featured Image
    url2 = "https://jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)
    soup = BeautifulSoup(browser.html, 'html.parser')
    
    image = soup.find("article", class_="carousel_item")["style"]
    image = image.replace("background-image: url('","")
    image = image.replace("');","")

    # Store image path in variable
    img_url = "https://jpl.nasa.gov"+image

    featured_image_url = img_url
    
    #Latest Tweet
    url3 = 'https://twitter.com/marswxreport?lang=en/'
    response = requests.get(url3)
    soup = BeautifulSoup(response.text, 'lxml')
    mars_weather = soup.find(class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text.strip()
    
    #Mars Facts
    url4 = 'https://space-facts.com/mars/'
    facts_df = pd.read_html(url4)[0]
    facts_df.columns = ["Datapoint","Value"]
    facts_df = facts_df.set_index(["Datapoint"])
    facts_df.columns.name = facts_df.index.name
    facts_df.index.name = None
    facts = facts_df.to_html()
    
    #Mars Hemispheres
    url3 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url3)
    soup = BeautifulSoup(browser.html, "html.parser")
    
    hemi_urls = []
    base_url = "https://astrogeology.usgs.gov"

    for div in soup.find("div", class_="full-content").find_all("div", class_="item"):
        hemi_urls.append(base_url + div.a["href"])
        
    hemi_list = []
    for link in hemi_urls:
        browser.visit(link)
        soup = BeautifulSoup(browser.html, "html.parser")
        hemi_name = soup.find("h2", class_="title").text
        hemi_image = soup.find("div", class_="downloads").find_all("li")[1].a["href"] + "/full.jpg"
        hemi_dict = {"img_url": hemi_image,
                        "title": hemi_name}
        hemi_list.append(hemi_dict)
        
    browser.quit()
    
    mars_dict = {
        "latest_title": title,
        "latest_news": paragraph_text,
        "featured_image": featured_image_url,
        "current_weather": mars_weather,
        "facts_html": facts,
        "hemispheres": hemi_list
    }
    
    return mars_dict