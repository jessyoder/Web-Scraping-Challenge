# Web-Scraping-Challenge

I built a web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page.

## Step 1 - Scraping

I completed my initial scraping using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter. This is shown in the file mission_to_mars.ipynb.

### NASA Mars News

* I scraped the NASA Mars News Site - https://mars.nasa.gov/news/ and collected the latest News Title and Paragraph Text

### JPL Mars Space Images - Featured Image

* I scraped the JPL Featured Space Image from https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars.

* I used splinter to navigate the site and find the image url for the current Featured Mars Image and assigned the url string to a variable called `featured_image_url`.

### Mars Facts

* I visited the Mars Facts webpage https://space-facts.com/mars/ and used Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.

* I then used Pandas to convert the data to a HTML table string.

### Mars Hemispheres

* I visited the USGS Astrogeology site https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars to obtain high resolution images for each of Mar's hemispheres.

* I wrote my code tovclick each of the links to the hemispheres in order to find the image url to the full resolution image.

* I saved both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. I used a Python dictionary to store the data using the keys `img_url` and `title`.

* I appended the dictionary with the image url string and the hemisphere title to a list.

## Step 2 - MongoDB and Flask Application

I used MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.

* I converting your Jupyter notebook into a Python script called `scrape_mars.py` with a function called `scrape_all` that will execute all of your scraping code from above and return one Python dictionary containing all of the scraped data.

* Next, I created a route called `/scrape` that will import your `scrape_mars.py` script and call your `scrape_all` function.

* I created a root route `/` that queries the Mongo database and pass the mars data into an HTML template to display the data.

* I create a template HTML file called `index.html` that takes the mars data dictionary and displays all of the data in the appropriate HTML elements.