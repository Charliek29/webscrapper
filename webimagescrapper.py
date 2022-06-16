from time import sleep
from bs4 import BeautifulSoup
import urllib.parse as urlparse
import requests
from fake_useragent import UserAgent
from random import randint


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
    imgs = bs_object.find_all('img')
    images_links = {}
    alt_set = set()

    for idx, tag in enumerate(imgs):
        dic = tag.attrs
        if 'alt' in dic.keys() and tag['alt'] not in alt_set:
            alt_set.add(tag['alt'])
            images_links[tag['alt']] = urlparse.urljoin(url, tag['src'])
        else:
            images_links[("unlabeled " + str(idx))] = urlparse.urljoin(url, tag['src'])
    return images_links


def find_all_links(url: str, bs_object: BeautifulSoup):
    # TODO add more logic here to check if the links are valid (using requests or another library)
    print(f'Looking for new links from {url[:70]}')
    links = bs_object.find_all('a')
    link_dic = {}
    for tag in links:
        link = tag['href']
        try:
            if requests.get(link).status_code == 200:
                name = tag.text
                link_dic[name] = link
        except:
            continue
    return link_dic


def display_image(img: str):
    print(f'loading image from this URL: {img}')
    response = requests.get(img)
    file = open("temp_img.png", "wb")
    file.write(response.content)
    sleep(1)
    file.close()


def manager(curr_dic: dict):
    vals = list(curr_dic.values())
    while len(vals) > 0:
        choice = randint(0, len(vals)-1)
        display_image(vals.pop(choice))


# make this multi-thread, one for searching for new links, one for getting images, one for viewer of images
if __name__ == "__main__":
    test = "https://www.google.com"
    # load_website(test)
    site = load_website(test)
    # print(site.prettify())
    img_w_url = find_all_images(test, site)
    new_links = find_all_links(test, site)
    manager(img_w_url)
