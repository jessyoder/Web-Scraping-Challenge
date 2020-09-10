# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

# Create a function for initiating the browser in Chrome
def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

# Create a function for scraping mars data
def scrape_all():

# Create dictionary for importing to Mongo
    mars_dict = {}

# Scrape Mars News: Nasa Article information
    # Open browser
    browser = init_browser()
    # Navigate to website
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)
    # Scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # Find articles
    nasa_articles = soup.find_all('div', class_='list_text')
    # Gather article title and article descriptoin
    nasa_title = soup.find('div', class_='content_title').text
    nasa_paragraph = soup.find('div', class_='rollover_description_inner').text
    # Put the article title and description into mars_dict
    mars_dict['nasa_title'] = nasa_title
    mars_dict['nasa_paragraph'] = nasa_paragraph
    # close the browser
    browser.quit()


# Scrape JPL Mars - Featured Image
    browser = init_browser()
    mars_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(mars_url)
    # Click the Full Image button
    browser.click_link_by_id('full_image')
    # Click the More Info button
    browser.click_link_by_partial_text('more info')
    # Wait for the page to load
    time.sleep(3)
    #Scrape page into mars_soup
    html = browser.html
    mars_soup = BeautifulSoup(html, 'html.parser')
    # Find featured image
    image_url = mars_soup.find('figure', class_='lede').a['href']
    featured_image_url = f'https://www.jpl.nasa.gov{image_url}'
    # Place featured image url into mars_dict
    mars_dict['featured_image_url'] = featured_image_url
    # Close the browser
    browser.quit()


# Scrape Mars facts
    browser = init_browser()
    mars_facts_url = 'https://space-facts.com/mars/'
    # Collect information from the html tables
    tables = pd.read_html(mars_facts_url)
    # Collect data from the first table
    mars_df = tables[0]
    # Rename column titles and set index as the description column
    mars_df.columns=['description', 'mars_info']
    mars_df.set_index('description', inplace=True)
    # Turn mars_df into something that can go into the html
    mars_df = mars_df.to_html()
    # Place table information into mars_dict
    mars_dict['mars_df'] = mars_df
    # Close the browser
    browser.quit()

# Scrape Mars Hemisphere titles and images
    browser = init_browser()
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)

    hemisphere_image_urls = []
    hemi_data = []

    for i in range(4):
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

    # Closer browser after scraping
    browser.quit()

    # Return results
    return mars_dict  