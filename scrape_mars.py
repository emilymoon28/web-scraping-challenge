from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import time

def init_browser():
    # https://splinter.readthedocs.io/en/latest/drivers/chrome.html
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape_info():
    
    #1. NASA Mars News
    #request response from the mars news webpage
    news_url='https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    news_response=requests.get(news_url)

    #create a BeautifulSoup object and define the parser
    news_soup=BeautifulSoup(news_response.text,'html.parser')
    title_div=news_soup.find('div',class_='content_title')
    news_title=title_div.a.text.strip()

    #news_title

    news_div=news_soup.find('div',class_='rollover_description_inner')
    news_p=news_div.text.strip()

    #news_p

    #2. JPL Mars Space Images - Featured Image
    browser=init_browser()
    jpl_url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    #brower will popup and visit the url
    browser.visit(jpl_url)
    time.sleep(5)

    #click "FULL IMAGE" to get the full image of the featured image
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')

    #now within 'FULL IMAGE' > 'more info' page
    full_html=browser.html
    jpl_soup=BeautifulSoup(full_html,'html.parser')
    img_figure=jpl_soup.find('figure',class_='lede')
    img_tag=img_figure.a.img

    img_base_url='https://jpl.nasa.gov'
    featured_img_url=img_base_url+img_tag['src']
    browser.quit()

    #featured_img_url

    #3. Mars Weather
    #open a new broswer
    browser=init_browser()
    weather_url='https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)

    # HTML Object.
    weather_html = browser.html

    # Parse HTML with Beautiful Soup
    weather_soup = BeautifulSoup(weather_html, "html.parser")
    
    tweet= weather_soup.find('div', attrs={'data-testid': 'tweet'})
    spans=tweet.find_all('span')
    weather_content=spans[4].text.replace("\n"," ")
    browser.quit()

    #weather_content

    #4. Mars Facts
    fact_url='https://space-facts.com/mars/'
    tables = pd.read_html(fact_url)

    #the 1st table on the website is the one we want
    fact_df=tables[0]

    #rename columns
    fact_df.columns = ['Description','Value']

    #reindex the dataframe
    fact_df.set_index('Description', inplace=True)

    #convert the datafram to html, and export to a file
    fact_table_html=fact_df.to_html()

    #fact_table_html

    #5. Mars Hemispheres
    #open a new broswer
    browser=init_browser()
    hem_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hem_url)

    # HTML Object.
    hem_html = browser.html

    # Parse HTML with Beautiful Soup
    hem_soup = BeautifulSoup(hem_html, "html.parser")

    image_links=hem_soup.find_all('div',class_='item')
    image_links_list=[link.a['href'] for link in image_links]

    hemisphere_image_urls=[]
    base_image_url='https://astrogeology.usgs.gov'
    for x in range(0,4):
        browser.visit(base_image_url+image_links_list[x])
        #give 2 seconds to fully load the page
        time.sleep(3)

        single_img_html = browser.html
        single_img_soup=BeautifulSoup(single_img_html,'html.parser')
        wide_img=single_img_soup.find('img',class_='wide-image')
        title=single_img_soup.find('h2',class_='title')

        #append each image links to the list
        hemisphere_image_urls.append({'title':title.text.replace(' Enhanced',''),
                                  'image_url':base_image_url+wide_img['src']})
    
    
        print(f'Done with the {x+1}th image')

    browser.quit()

    #hemisphere_image_urls

    #store all result in a dictionary and it is just one record in the MongoDB collection
    mars_data={
        'news_title':news_title,
        'news_p':news_p,
        'featured_image_url':featured_img_url,
        'mars_weather':weather_content,
        'fact_table_html': fact_table_html,
        #list of dictionaries
        'hemisphere_image_urls':hemisphere_image_urls
    }

    #return results
    return mars_data


