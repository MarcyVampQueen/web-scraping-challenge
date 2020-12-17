from bs4 import BeautifulSoup
from splinter import Browser
import time
import pandas as pd

def scrape():
    # Setup browser
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)

    # Get the webpage for scraping articles and pass to Soup
    browser.visit("https://mars.nasa.gov/news")
    time.sleep(2)
    soup = BeautifulSoup(browser.html, 'html.parser')

    # Get the first article on the page
    news_title = soup.find_all('div', class_='content_title')[1].text
    news_p = soup.find_all('div', class_='article_teaser_body')[0].text

    # Visit the next site for images
    browser.visit("https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars")
    time.sleep(2)
    browser.links.find_by_partial_text('FULL').click()
    browser.links.find_by_partial_text('more info').click()

    # Get the featured image
    soup = BeautifulSoup(browser.html, 'html.parser')
    featured_image_url = "https:" + soup.find_all('div', class_='download_tiff')[1].a['href']

    # Visit the next site for Mars facts
    browser.visit("https://space-facts.com/mars/")
    time.sleep(2)
    soup = BeautifulSoup(browser.html, 'html.parser')
    table = soup.find('table', id="tablepress-p-mars-no-2").find_all('tr')

    mars_info = []
    for row in table:
        info = row.text.split(':')
        mars_info.append({
            "Attribute":info[0],
            "Info":info[1]
        })
    table_html = pd.DataFrame(mars_info).to_html()

    # Visit the next site for hemispheres and grab all the links
    browser.visit("https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")
    time.sleep(1)
    soup = BeautifulSoup(browser.html,'html.parser')
    links = soup.find_all('a', class_="itemLink product-item")

    # Visit all of the links, collecting images along the way (every other link is an image, so skip it)
    images = []
    for page in links[1::2]:
        browser.visit("https://astrogeology.usgs.gov/" + page["href"])
        time.sleep(2)
        soup = BeautifulSoup(browser.html,'html.parser')

        images.append({
            "title":page.h3.text,
            "url":"https://astrogeology.usgs.gov" + soup.find('img', class_='wide-image')["src"]
        })
        
    browser.quit()

    mars_content = {
        "title":news_title,
        "content":news_p,
        "feature":featured_image_url,
        "facts":table_html,
        "images":images
    }

    return mars_content



# def get_url(url):