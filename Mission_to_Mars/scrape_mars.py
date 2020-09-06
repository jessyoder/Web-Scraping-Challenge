from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # Scrape Nasa Article information
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)

    html = browser.html
    nasa_soup = BeautifulSoup(html, 'html.parser')

    nasa_articles = nasa_soup.find_all('div', class_='list_text')

    for articles in nasa_articles:
        nasa_title = articles.find('div', class_='content_title').text
        nasa_paragraph = articles.find('div', class_='article_teaser_body').text
        
        print('------------------------')
        print(nasa_title)
        print(nasa_paragraph)

    # Scrape JPL Mars featured image
    mars_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(mars_url)

    browser.click_link_by_id('full_image')

    html = browser.html
    mars_soup = BeautifulSoup(html, 'html.parser')

    featured_image_url = mars_soup.find('img', class_='fancybox-image')['src']
    base_url = (mars_url.split('/space'))[0]
    featured_url = base_url+featured_image_url

    # Scrape Mars facts
    mars_facts_url = 'https://space-facts.com/mars/'

    tables = pd.read_html(mars_facts_url)
    tables

    mars_df = tables[0]
    mars_df

    # Scrape Mars Hemisphere titles and images
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)

    hemisphere_image_urls = []
    hemi_data = []

    for i in range(4):
        browser.find_by_css("a.product-item h3")[i].click()

        hemi_soup = BeautifulSoup(browser.html, "html.parser")
        try:
            title = hemi_soup.find("h2", class_="title").get_text()
            sample = hemi_soup.find("a", text="Sample").get("href")
        except AttributeError:
            title = None
            sample = None
        hems = {
            "title": title,
            "img_url": sample
        }
        hemi_data.append(hems)
        hemisphere_image_urls.append(sample)
        
        browser.back()
        
    hemi_data

    mars_dict = {'News Title': nasa_title,
                'News Paragraph': nasa_paragraph,
                'Featured Image': featured_url,
                'Mars Data': mars_df,
                'Image Title': hemi_data,
                'Image URL': hemisphere_image_urls
                }