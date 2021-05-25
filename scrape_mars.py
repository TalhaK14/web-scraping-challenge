from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import numpy as np
import pandas as pd
import re

def init_browser():
    executable_path = {'executable_path': 'C:\\Users\\ktalh\\Downloads\\chromedriver_win32\\chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
def scrape():
    browser=init_browser()
    mars_dict={}

    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')

    news_title = news_soup.find_all('div', class_='content_title')[0].text
    news_p = news_soup.find_all('div', class_='rollover_description_inner')[0].text

    jpl_nasa_url = 'https://www.jpl.nasa.gov'
    images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(images_url)
    html = browser.html
    images_soup = BeautifulSoup(html, 'html.parser')

    relative_image_path = images_soup.find_all('img')[3]["src"]
    featured_image_url = jpl_nasa_url + relative_image_path

    facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(facts_url)
    tables

    mars_facts_df = tables[2]
    mars_facts_df.columns = ["Description", "Value"]
    mars_facts_df

    mars_html_table = mars_facts_df.to_html()
    mars_html_table

    mars_html_table.replace('\n', '')

    usgs_url = 'https://astrogeology.usgs.gov'
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    hemispheres_html = browser.html
    hemispheres_soup = BeautifulSoup(hemispheres_html, 'html.parser')

    all_mars_hemispheres = hemispheres_soup.find('div', class_='collapsible results')
    mars_hemispheres = all_mars_hemispheres.find_all('div', class_='item')

    hemisphere_image_urls = []

    for i in mars_hemispheres:
        hemisphere = i.find('div', class_="description")
        title = hemisphere.h3.text
        hemisphere_link = hemisphere.a["href"]    
        browser.visit(usgs_url + hemisphere_link)
        image_html = browser.html
        image_soup = BeautifulSoup(image_html, 'html.parser')
        image_link = image_soup.find('div', class_='downloads')
        image_url = image_link.find('li').a['href']
        image_dict = {}
        image_dict['title'] = title
        image_dict['img_url'] = image_url
        hemisphere_image_urls.append(image_dict)

    mars_dict = {
            "news_title": news_title,
            "news_p": news_p,
            "featured_image_url": featured_image_url,
            "fact_table": str(mars_html_table),
            "hemisphere_images": hemisphere_image_urls
        }

    browser.quit()
    return mars_dict


