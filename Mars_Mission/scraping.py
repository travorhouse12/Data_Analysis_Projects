# Import SPlinter and BeautifulSoup 
from splinter import Browser 
from bs4 import BeautifulSoup as soup 
import pandas as pd
import datetime as dt 
browser = Browser("chrome", executable_path="chromedriver", headless=True)


# Initiate the browser 
def scrape_all():
    # Initialize headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    
    
    # store hemisphere data as a list of dictionaries, one dictionary for each hemisphere data.
    mars_hemi_lst = list()
    names = ['Cerberus','Schiaparelli', 'Syrtis Major','Valles Marineris']
    for name in names:
        # call scraping fuction for each hemisphere
        hemi_title, hemi_img_url = mars_hemispheres(browser, name)
       # add scraped data into dictionary
        hemi_dict = {"img_url":hemi_img_url, "title": hemi_title}
        # add each dictionary into list
        mars_hemi_lst.append(hemi_dict)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary 
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemi_data": mars_hemi_lst
    }

    # Stop webdriver and return data 
    browser.quit()
    return data

def mars_hemispheres(browser, hemi_name):
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)
    # STEP 1: click '... Hemisphere Enhanced'button
    browser.is_element_present_by_text(f'{hemi_name} Hemisphere Enhanced', wait_time = 1)
    browser.click_link_by_partial_text(f'{hemi_name} Hemisphere Enhanced')
    
    # STEP 2: BeautifulSoup to parse and extract image url
    soup_1 = soup(browser.html, 'html.parser')
    try:
        rel_url = soup_1.select_one('img.wide-image').get('src')
        title = soup_1.select_one('h2.title').text
    except AttributeError:
        return None
    # STEP 3: combine as an absolute url
    img_url = f'https://astrogeology.usgs.gov{rel_url}'
    
    return title, img_url



def mars_news(browser):

    # Visit the mars nasa news site 
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page 
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling 
    try:

        slide_elem = news_soup.select_one('ul.item_list li.slide')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text 
        news_p = slide_elem.find("div", class_='content_title').get_text()

    
    except AttributeError:
        return None, None
        
    return news_title, news_p


# ### Featured Images 

def featured_image(browser):

    # Visit URL 
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')[0]
    full_image_elem.click()

    # Find the more info button and click that 
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()


    # Parse the resulting html with soup 
    html = browser.html 
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling 
    try:

        # Find the relative image url 
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    
    except AttributeError:
        return None
    

    # Use the base URL to create an absolute URL 
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    
    return img_url

# Mars Facts

def mars_facts():

    try:
        # use "read_html" to scrape the facts table into a dataframe
        df = pd.read_html('https://space-facts.com/mars/')[0]
    except BaseException:
        return None

    # Assign columns and set index of dataframe 
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)
        
    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

if __name__ == "__main__":
    # If running as script, print scraped data 
    print(scrape_all())






