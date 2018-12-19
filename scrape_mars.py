# Import Dependencies
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from splinter import Browser
import time


def init_browser():
    # set exec path for chromedriver
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


def scrape_info():
    browser = init_browser()
    
    ## Mars News ##
    # set url
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # get html from current window
    html = browser.html

    # make soup
    soup = bs(html, 'html.parser')

    # get first title
    news_title = soup.find('div',class_="content_title").text

    # get first paragraph
    news_p = soup.find('div',class_="article_teaser_body").text
    
    ## JPL Image Scrape ##
    # set jpl url
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    # navigate to url
    browser.visit(jpl_url)

    # add wait for good measure..
    time.sleep(1)

    # find the image
    browser.find_by_id('full_image').first.click()

    # another wait...
    time.sleep(2)

    # click details link
    browser.click_link_by_partial_href('details')

    # wait some more...
    time.sleep(1)

    # set current browser html
    img_html = browser.html

    # make soup
    img_soup = bs(img_html,'lxml')
    # print(img_soup.prettify())

    # set image url
    featured_image_url = 'http://jpl.nasa.gov' + img_soup.find('img',class_='main_image')['src']
    #print(featured_image_url)
    
    ## Mars Twitter ##
    # set mars weather twitter url
    mars_wthr_url = 'https://twitter.com/marswxreport?lang=en'

    # visit url
    browser.visit(mars_wthr_url)

    # add wait to let page load
    time.sleep(1)

    # grab current window html
    mars_wthr_html = browser.html

    # make soup
    twtr_soup = bs(mars_wthr_html,'html.parser')

    # print(twtr_soup.prettify())

    # find tweets
    tweets = twtr_soup.find_all('li',{'class':'js-stream-item stream-item stream-item '})

    # find first/latest weather tweet (to move past retweeted posts)
    for tweet in tweets:
        # set content user
        content_u = tweet.find('span',{'class':'username u-dir u-textTruncate'}).text

        # set weather tweet
        mars_weather = tweet.find('p').text

        # see results
        print(content_u)
        print(mars_weather)

        # find original post and break when found
        if content_u == '@MarsWxReport':
            break
            
    ## Pandas Scraping ##
    # set url for pd scrape
    mars_facts_url = 'https://space-facts.com/mars/'

    # read html with pandas
    fact_tbls = pd.read_html(mars_facts_url)

    # list to df
    fact_df = fact_tbls[0]

    # set headers
    fact_df.columns = ['Attribute','Value']

    # set index in place
    fact_df.set_index('Attribute',inplace=True)

    # set to html table
    fact_df_html = fact_df.to_html(escape=False)

    # strip new lines chars
    cln_fact_df_html = fact_df_html.replace('\n','')

    ## Mars Hemisphere Scrape ##
    # mars hemisphere url
    mars_hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # browser load and scrape
    browser.visit(mars_hem_url)

    # add wait for safe measures
    time.sleep(1)

    # make some soup
    hem_soup = bs(browser.html,'lxml')

    # find all links
    thumb_list = hem_soup.find_all('div',{'class':'description'})

    # set partial link (prefix)
    part_link = 'https://astrogeology.usgs.gov'

    # create empty list
    mars_hems = []

    # loop through thumbnail list
    for t in thumb_list:
        # set link text variable
        lnk = t.find('h3').text
        # print to see which hem is clicking...
        print(f'>>>>>searching for *{lnk}*<<<<<')
        # click link with text
        browser.click_link_by_partial_text(lnk)
        # make temp soup
        temp_soup = bs(browser.html,'lxml')
        # assign temp variables from soup search
        img = temp_soup.find('img','wide-image')
        div2 = temp_soup.find('div','content')
        # create dict
        t_dict = {'img_url':part_link + img['src'],
                  'title':div2.h2.text}
        # add to list
        mars_hems.append(t_dict)
        # go back
        browser.click_link_by_partial_text('Back')
    
    # store mars data
    mars_data = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'mars_weather': mars_weather,
        'mars_facts': cln_fact_df_html,
        'mars_hems': mars_hems
    }
    
    # close browser
    browser.quit()
    
    # return
    return mars_data