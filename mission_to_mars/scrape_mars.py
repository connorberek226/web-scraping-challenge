import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser

def scrape():

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


    
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    news = soup.find("li", class_="slide")
    news_title = news.find("h3").text
    news_p = news.find(class_="article_teaser_body").text


     
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(url)


    html = browser.html
    soup = bs(html, 'html.parser')

    main_feature_body = soup.find(class_="centered_text clearfix main_feature primary_media_feature single").find(class_="carousel_items").article["style"]
    feature_image = main_feature_body.split()[1].strip("url('');")

    feature_image_url = "https://jpl.nasa.gov" + feature_image



    url = 'https://space-facts.com/mars/'

    tables = pd.read_html(url)
    factoids = tables[0]
    factoids.columns = ["Measurement", "Value"]

    html_factoids = factoids.to_html()

    html_factoids.replace('\n', '')



    parent_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


    browser.visit(parent_url)


    html = browser.html
    soup = bs(html, 'html.parser')

    base_url = "https://astrogeology.usgs.gov"
    links = [base_url + link.a["href"] for link in soup.find_all("div", class_="item")]


    hemisphere_image_url = []

    for link in links:
    
        browser.visit(link)
        html = browser.html
        soup = bs(html, 'html.parser')
    
        img_url = base_url + soup.find("img", class_="wide-image")["src"]
        title = soup.find(class_="content").find("h2").text
    
        hemisphere_image_url.append({"title: ": title, "iamge_url: ": img_url})

    browser.quit()


    mars_info = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": feature_image_url,
        "mars_factoids": html_factoids,
        "hemisphere_image_url": hemisphere_image_url
    }

    return mars_info