#!/usr/bin/python

# mission_to_mars.ipynb
# Eric Staveley  MWsa

# Start by converting your Jupyter notebook into a Python script called scrape_mars.py
# with a function called scrape that will execute all of your scraping code
# and return one Python dictionary containing all of the scraped data.


from bs4 import BeautifulSoup
import pandas as pd
from splinter import Browser
import time


# declare the new Python dictionary containing our scrapes
mars_dict = {}

# Mac user [prob TA/Instr  :-) ]
# Choose the executable path to driver
# executable_path = {'executable_path': '/usr/local/bin/chromedriver.exe'}
# browser = Browser('chrome', **executable_path, headless=False)


def init_browser():
    # windows (me)   Make sure the chromedriver is in the jupy nb file location
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():

    try:
        # # NASA Mars News Scraping

        # Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text.
        # Assign the text to variables that you can reference later.

        print("Beginning NASA mars news scraping")
        browser = init_browser()

        # NASA mars url
        url_mars = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

        # confirm the site
        browser.visit(url_mars)

        # time delay
        time.sleep(2)

        # define html object
        html_mars = browser.html

        # use BeautifulSoup to extract data from html
        soup_mars = BeautifulSoup(html_mars, 'lxml')

        # get latest news title and show it
        news_title = soup_mars.find('div', class_='content_title').text
        # news_title

        # find unique tag and get latest news paragraph and show it
        news_paragraph = soup_mars.find(
            'div', class_='article_teaser_body').text
        # news_paragraph

        # add to our new dict
        mars_dict['news_title'] = news_title
        mars_dict['news_paragraph'] = news_paragraph

    finally:
        # browser.quit()  # close the browser to avoid multiple instances
        print("Finsihed NASA mars news scraping")

        print(mars_dict)

    # # JPL Scraping

    # Visit the url for JPL Featured Space Image
    # Use splinter to navigate the site and find the image url for the current
    # Featured Mars Image and assign the url string to a variable called featured_image_url.
    # Make sure to find the image url to the full size .jpg image.
    # Make sure to save a complete url string for this image.

    try:

        print("Beginning JPL image scraping")
        #browser = init_browser()
        # Find mars images from JPL url
        url_jpl = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

        # define base jpl url
        base_url = 'https://www.jpl.nasa.gov/'

        # confirm the site
        browser.visit(url_jpl)
        # time delay
        time.sleep(2)

        # use is_text_present and click_link_by_partial_text to help define browser
        browser.is_text_present('FULL IMAGE')
        browser.click_link_by_partial_text('FULL IMAGE')

        # define html object
        html_jpl = browser.html

        # use BeautifulSoup to extract data from html
        soup_jpl = BeautifulSoup(html_jpl, 'lxml')

        # find unique tag from style to locate data of interest
        image_location = soup_jpl.find('article')['style'].replace(
            'background-image: url(', '').replace(');', '')[1:-1]
        # image_location

        featured_image_url = base_url + image_location
        # featured_image_url    #  the full image url

        # add to our new dict
        mars_dict['featured_image_url'] = featured_image_url

    finally:
        # browser.quit()  # close the browser to avoid multiple instances
        print("Finished JPL image scraping")
        print(mars_dict)

    # # Scrape Mars Weather twitter site

    # Visit the Mars Weather twitter account and scrape the latest Mars weather tweet from the page.
    # Save the tweet text for the weather report as a variable called mars_weather.

    try:

        print("Beginning Mars twitter weather scraping")
        #browser = init_browser()

        # scrape mars weather from their twitter account
        url_mars_weather = 'https://twitter.com/marswxreport?lang=en'
        # verify site
        browser.visit(url_mars_weather)

        # time delay
        time.sleep(2)

        # define html object
        html_mars_weather = browser.html

        # use BeautifulSoup to extract data from html
        soup_mars_weather = BeautifulSoup(html_mars_weather, 'lxml')

        # find unique tag to locate data of interest, weather info is just below div class js-tweet-text-container
        weather_info = soup_mars_weather.find_all(
            'div', class_='js-tweet-text-container')
        weather_info

        # some tweets may not be about the weather....so we will loop thru
        # until we find 'sol' 'high' 'low' and 'pressure' strings
        for item in weather_info:
            tweet_weather = item.find('p').text
            if 'sol' and 'low' and 'high' and 'pressure' in tweet_weather:
                break   # can stop looking
            # tweet_weather

        # strip new line char and trim off pic and beyond, and  and save as mars_weather
        temp = tweet_weather.replace('\n', ' ')
        new_temp = temp[:temp.rfind('pic')]
        mars_weather = new_temp
        mars_weather

        # add to our new dict
        mars_dict['mars_weather'] = mars_weather

    finally:
        # browser.quit()  # close the browser to avoid multiple instances
        print("Finished Mars twitter weather scraping")
        print(mars_dict)

    # # Scrape Mars facts url
    # Visit the Mars Facts webpage and use Pandas to scrape the table containing facts
    # about the planet including Diameter, Mass, etc.
    # Use Pandas to convert the data to a HTML table string.

    try:
        print("Beginning Mars facts page scraping to html table")

        # scrape mars facts page using pandas
        url_facts = 'https://space-facts.com/mars/'

        # parse the url with read_html
        mars_tables = pd.read_html(url_facts)
        # mars_tables

        # time delay
        time.sleep(2)

        # make the mars fact df out of the mars_table list
        df = mars_tables[0]
        # df

        # df = mars_tables[0]
        df.columns = ['Description', 'Value']

        # set to make header left justified and set to False for index stuff
        html_tbl_str = df.to_html(
            index_names=False, index=False, justify='left')

        # add to our new dict
        mars_dict['mars_facts_table'] = html_tbl_str
        # except Exception as e:
    finally:
        pass
        print("Finished Mars facts page scraping to html table")
        print(mars_dict)

        # # Get images of Mars hemispheres from USGS Astrogeology url

        # Visit the USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres.
        # You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
        # Save both the image url string for the full resolution hemisphere image, and
        # the Hemisphere title containing the hemisphere name.
        # Use a Python dictionary to store the data using the keys img_url and title.

        # Append the dictionary with the image url string and the hemisphere title to a list.
        # This list will contain one dictionary for each hemisphere.

    try:
        print("Beginning USGS Mars hemisphere image extraction")
        #browser = init_browser()
        # define url
        usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        # verify
        browser.visit(usgs_url)

        # time delay
        time.sleep(2)

        # define base url
        hemis_base_url = 'https://astrogeology.usgs.gov'

        # define html object
        html_hemis = browser.html

        # use BeautifulSoup to extract data from html
        soup_jpl = BeautifulSoup(html_hemis, 'lxml')

        # find unique tag to locate data of interest
        cls_item = soup_jpl.find_all('div', class_='item')

        # make/clear empty list to hold our image list
        hemis_img_list = []

        for item in cls_item:
            # hemisphere titles found in h3 tag
            img_title = item.find('h3').text

            # find sub url of image, found in cls itemLink product-item
            sub_img_url = item.find(
                'a', class_='itemLink product-item')['href']

            # need to look into each of the links to the hemispheres in order to get final link
            browser.visit(hemis_base_url + sub_img_url)
            # time delay
            time.sleep(2)

            # now define html object
            img_html = browser.html

            # use BeautifulSoup to extract data from html
            soup_img = BeautifulSoup(img_html, 'lxml')
            # the specific image path ending
            endpoint = soup_img.find('img', class_='wide-image')['src']
            # print(endpoint)

            # construct the image url to the full resolution image
            img_url = hemis_base_url + endpoint

            # append to our list we created
            hemis_img_list.append({"title": img_title, "img_url": img_url})

            # add to our new dict
            mars_dict['hemis_img_list'] = hemis_img_list
    finally:
        browser.quit()
        print("Finished USGS Mars hemisphere image extraction")
        print(mars_dict)

    #print("mars_dict within function:\n")
    # print(mars_dict)
    return mars_dict   # can now return the assembled dict

# end of function scrape

# comment out the below 4 lines when rolling into our software suite!
#print("Invoking the scrape function...")
# scrape()
#print("\nFinal contents of mars_dict outside function:\n")
# print(mars_dict)
