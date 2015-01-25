"""
A data gathering workflow for The Bachelor
"""

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import pickle
from os.path import join

PICKLEDIR = "./pickles/"


def pickle_indiv_pages(url, ofile):
    """
    gather information about an individual person
    :param url:
    :return:
    """
    browser = webdriver.Firefox()

    browser.get(url)
    in_dat = browser.page_source
    write_dict = dict({"url": url,
                       "content": in_dat})
    opickle = file("pickle_page.pickle", 'w')
    pickle.dump(write_dict, opickle)
    opickle.close()
    browser.quit()


def get_main_links():
    """
        Go into the main page, grab all the profiles, download their pictures, and save everything else.
    """

    main_page = "http://abc.go.com/shows/the-bachelor"
    main_data = requests.get(main_page)
    bs_text = BeautifulSoup(main_data.text)
    profiles = bs_text.find_all('a', class_='imageContainer')

    ret_data = list()

    for p in profiles:
        cast_link = p['href']
        if cast_link.find("cast/19-") > -1:
            ret_data.append(cast_link)
    return ret_data


if __name__ == '__main__':
    # get_main_links()
    links = get_main_links()
    for index, link in enumerate(links):
        print link, index
        pickle_indiv_pages(link, join(PICKLEDIR, str(index) + ".pickle"))
    # pickle_indiv_pages("http://abc.go.com/shows/the-bachelor/cast/19-bachelorette-alissa", join(PICKLEDIR, '1.pickle'))
