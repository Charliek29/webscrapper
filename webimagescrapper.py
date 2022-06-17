from time import sleep
from bs4 import BeautifulSoup
import urllib.parse as urlparse
import requests
from fake_useragent import UserAgent
from random import randint
from matplotlib import pyplot as plt
from matplotlib import image as mpimg
import re


def load_website(url: str):
    print(f'Starting scrape of {url[:70]}')
    ua = UserAgent()
    header = {'User-Agent': str(ua.chrome)}
    html = requests.get(url, headers=header)
    if html.status_code == 200:
        return BeautifulSoup(html.text, 'html.parser')
    else:
        return None


def find_all_images(url: str, bs_object: BeautifulSoup):
    print(f'Getting all images from {url[:70]}')
    html = bs_object.prettify()
    # pat = re.compile(r'<img [^>]*src="([^"]+)')
    pat = re.compile(r'<img (?:alt)?.*\"(http[\_A-Za-z0-9.\/\-\:\?=]*)\".*\/>')
    img = pat.findall(html)
    return img


def find_all_links(url: str, bs_object: BeautifulSoup):
    print(f'Looking for new links from {url[:70]}')
    links = bs_object.find_all('a')
    link_dic = {}
    for tag in links:
        try:
            link = tag['href']
            if requests.get(link).status_code == 200:
                name = tag.text
                link_dic[name] = link
        except:
            continue
    return link_dic


def display_image(link_to_photo: str):
    print(f'loading image from this URL: {link_to_photo}')
    response = requests.get(link_to_photo)
    file = open("temp_img.jpg", "wb")
    file.write(response.content)
    file.close()
    try:
        image = mpimg.imread("temp_img.jpg")
        plt.imshow(image)
        plt.show()
        sleep(1)
    except:
        print('Skipping one image')
    # plt.close('all')


def manager(lst: list):
    while len(lst) > 0:
        choice = randint(0, len(lst) - 1)
        display_image(lst.pop(choice))


# make this multi-thread, one for searching for new links, one for getting images, one for viewer of images
if __name__ == "__main__":
    test = "https://www.google.com"
    site = load_website(test)
    # print(site.prettify())
    img_w_url = find_all_images(test, site)
    # print(img_w_url)
    # new_links = find_all_links(test, site)
    manager(img_w_url)
