"""
A data gathering workflow for The Bachelor
"""

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import pickle
from os.path import join

PICKLEDIR = "../pickles/"


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
    opickle = file(ofile, 'w')
    pickle.dump(write_dict, opickle)
    opickle.close()
    browser.quit()


def individual_extract(pfile_name):
    """
    given a pickle file, extract some data from it
    :param pfile_name:
    :return:
    """

    pfile = file(pfile_name, 'r')
    in_dat = pickle.load(pfile)
    pfile.close()

    ret_vals = dict()

    bs = BeautifulSoup(in_dat['content'])
    descript = bs.find("div", class_='descriptionBody')
    status = bs.find("h2", class_='itemMeta').text.split(" - ")
    if len(status) == 2:
        ret_vals['eliminated'] = True
        ret_vals['goneweek'] = int(status[1].strip()[-1:])
    else:
        ret_vals['eliminated'] = False

    name = bs.find("h1", class_='title').text
    ret_vals['name'] = name.strip()

    prof_photo = bs.find("div", class_="info").find("img")
    ret_vals['photo_url'] = prof_photo['src']

    item_list = str(descript).split("<br/>")
    ret_vals['age'] = item_list[0].strip()[-2:]

    occ_html = BeautifulSoup(item_list[1])
    ret_vals['occupation'] = occ_html.text.split(":")[1].strip()

    hometown_html = BeautifulSoup(item_list[2])
    hometown = hometown_html.text.split(":")[1].strip().split(",")
    ret_vals['hometown_name'] = hometown[0]
    try:
        ret_vals['hometown_state'] = hometown[1]
    except:
        ret_vals['hometown_state'] = 'UNK'

    height = BeautifulSoup(item_list[3]).text.split(":")[1].replace('"', '').split("'")
    height_inches = int(height[0]) * 12 + int(height[1])
    ret_vals['height_inches'] = height_inches

    txt_num_tats = BeautifulSoup(item_list[4]).text.split(":")[1].strip()
    try:
        num_tats = int(txt_num_tats)
    except:
        num_tats = 0

    print num_tats

    return ret_vals



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


def gather_all_pages():
    """
    gather links and data for all the pages
    :return:
    """
    links = get_main_links()
    for index, link in enumerate(links):
        print link, index
        newfile = join(PICKLEDIR, str(index) + ".pickle")
        print newfile
        pickle_indiv_pages(link, newfile)


if __name__ == '__main__':
    # pf1 = join(PICKLEDIR, '0.pickle')
    # individual_extract(pf1)
    for i in range(0, 28):
        tgt_file = join(PICKLEDIR, str(i) + ".pickle")
        individual_extract(tgt_file)
