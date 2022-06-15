# web image scraper and finder
from bs4 import BeautifulSoup 
import requests
import os
import urllib.parse as urlparse
import time
from selenium import webdriver


def load_website(site: str):
    print(f'Starting scrape of {site[:70]}')
    # TODO FIX THIS PART USING THESE LINKS BELOW
    # https://stackoverflow.com/questions/41501636/how-to-install-pip3-on-windows
    # https://stackoverflow.com/questions/64717302/deprecationwarning-executable-path-has-been-deprecated-selenium-python
    # https://stackoverflow.com/questions/42524114/how-to-install-geckodriver-on-a-windows-system
    browser = webdriver.Edge("F:\Downloads\edgedriver_win32\msedgedriver.exe")
    browser.get(site)
    html = browser.page_source
    time.sleep(2)
    # close web browser
    browser.close()
    browser.quit()
    return BeautifulSoup(html, 'html.parser') # TODO make sure this return is correct with multiple images
        

def find_all_images(url: str, bs_object: BeautifulSoup):
    print(f'Getting all images from {url[:70]}')
    imgs = bs_object.find_all('img')
    images_links = {}
    alt_set = set()
    
    for idx, tag in enumerate(imgs):
        if tag['alt'] not in alt_set:
            alt_set.add(tag['alt'])
            images_links[tag['alt']] = urlparse.urljoin(url, tag['src']) 
        else:
           images_links[(tag['alt']+str(idx))] = urlparse.urljoin(url, tag['src']) 
    return images_links


def find_all_links(url:str, bs_object: BeautifulSoup):
    print(f'Looking for new links from {url[:70]}')
    links = bs_object.find_all('a')
    link_dic = {}
    for tag in links:
        link = tag['href']
        name = tag.text
        link_dic[name] = link
    return link_dic


def display_image(img: str):
    pass

# make this multi-thread, one for searching for new links, one for getting images, one for viewer of images
if __name__ == "__main__":
    test = "https://www.duolingo.com"
    # load_website(test)
    site = load_website(test)
    print(site.prettify())
    # img_w_url = find_all_images(test, site)
    # print(len(img_w_url))
    # new_links = find_all_links(test, site)
    # print(new_links)