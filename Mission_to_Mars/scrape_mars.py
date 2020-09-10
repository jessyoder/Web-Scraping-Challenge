from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape_all():

    # Create dictionary for importing to Mongo
    mars_dict = {}

    
    # Scrape Mars News: Nasa Article information
    browser = init_browser()
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    nasa_articles = soup.find_all('div', class_='list_text')

    # nasa_title = nasa_articles.find('div', class_='content_title').text
    # nasa_paragraph = nasa_articles.find('div', class_='article_teaser_body').text
    nasa_title = soup.find('div', class_='content_title').text
    nasa_paragraph = soup.find('div', class_='rollover_description_inner').text

    mars_dict['nasa_title'] = nasa_title
    mars_dict['nasa_paragraph'] = nasa_paragraph

    browser.quit()


    # Scrape JPL Mars - Featured Image
    browser = init_browser()
    mars_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(mars_url)

    # Click the Full Image button
    browser.click_link_by_id('full_image')

    # Click the More Info button
    browser.click_link_by_partial_text('more info')

    time.sleep(5)

    html = browser.html
    mars_soup = BeautifulSoup(html, 'html.parser')

    image_url = mars_soup.find('figure', class_='lede').a['href']
    featured_image_url = f'https://www.jpl.nasa.gov{image_url}'

    mars_dict['featured_image_url'] = featured_image_url

    browser.quit()


    # Scrape Mars facts
    browser = init_browser()
    mars_facts_url = 'https://space-facts.com/mars/'

    tables = pd.read_html(mars_facts_url)

    mars_df = tables[0]
    mars_df.columns=['description', 'mars_info']
    mars_df.set_index('description', inplace=True)
    mars_df = mars_df.to_html()

    mars_dict['mars_df'] = mars_df

    browser.quit()

    # Scrape Mars Hemisphere titles and images
    browser = init_browser()
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)

    hemisphere_image_urls = []
    hemi_data = []

    for i in range(4):
#     browser.find_by_css("a.product-item h3")[i].click()
        browser.find_by_css("h3")[i].click()

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
        
    mars_dict['hemi_data'] = hemi_data
    mars_dict['hemisphere_image_urls'] = hemisphere_image_urls

    # Store data in a dictionary
    # mars_dict = {'News Title': nasa_title,
    #             'News Paragraph': nasa_paragraph,
    #             'Featured Image': featured_url,
    #             'Mars Data': mars_df,
    #             'Image Title': hemi_data,
    #             'Image URL': hemisphere_image_urls
    #             }  

    # Closer browser after scraping
    browser.quit()

    # Return results
    return mars_dict  