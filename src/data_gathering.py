"""
A data gathering workflow for The Bachelor
"""

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import pickle
from os.path import join
import json

PICKLEDIR = "../pickles/"
IMAGEDIR = "../images/"
DATADIR = "../data/"


def convert_text_to_num(text):
    """
    convert a word of text to a number
    :param text: text of a number
    :return:
    """
    conversion = dict({"none": 0,
                       "zero": 0,
                       "one": 1,
                       "two": 2,
                       "three": 3,
                       "four": 4,
                       "five": 5,
                       "six": 6,
                       "seven": 7,
                       "eight": 8,
                       "nine": 9,
                       "ten": 10,
                       "eleven": 11,
                       "twelve": 12})
    try:
        ret_val = conversion[text.strip().lower()]
    except KeyError:
        ret_val = -1
    return ret_val


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

    data_soup = BeautifulSoup(in_dat['content'])
    descript = data_soup.find("div", class_='descriptionBody')
    status = data_soup.find("h2", class_='itemMeta').text.split(" - ")
    if len(status) == 2:
        ret_vals['eliminated'] = True
        ret_vals['goneweek'] = int(status[1].strip()[-1:])
    else:
        ret_vals['eliminated'] = False

    name = data_soup.find("h1", class_='title').text
    ret_vals['name'] = name.strip()

    prof_photo = data_soup.find("div", class_="imageContainer").find("img")
    ret_vals['photo_url'] = prof_photo['src']

    item_list = str(descript).split("<br/>")
    ret_vals['age'] = int(item_list[0].strip()[-2:])

    occ_html = BeautifulSoup(item_list[1])
    ret_vals['occupation'] = occ_html.text.split(":")[1].strip()

    hometown_html = BeautifulSoup(item_list[2])
    hometown = hometown_html.text.split(":")[1].strip().split(",")
    ret_vals['hometown_name'] = hometown[0]
    try:
        ret_vals['hometown_state'] = hometown[1]
    except IndexError:
        ret_vals['hometown_state'] = 'UNK'

    height = BeautifulSoup(item_list[3]).text.split(":")[1].replace('"', '').split("'")
    height_inches = int(height[0]) * 12 + int(height[1])
    ret_vals['height_inches'] = height_inches

    txt_num_tats = BeautifulSoup(item_list[4]).text.split(":")[1].strip()
    try:
        num_tats = int(txt_num_tats)
    except ValueError:
        num_tats = convert_text_to_num(txt_num_tats)

    ret_vals['num_tattoos'] = num_tats

    likes = BeautifulSoup(item_list[5]).text.split(":")[1].split(",")
    ret_vals['likes'] = [str(_).strip() for _ in likes]

    datefear = BeautifulSoup(item_list[6]).text.split(":")[1]
    ret_vals['date_fear'] = datefear

    ret_vals['free_text'] = BeautifulSoup(' '.join(item_list[7:])).text

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

    for profile in profiles:
        cast_link = profile['href']
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


def download_images(in_dat_dict):
    """
    takes a data dict from individual_extract() and downloads the images to a folder
    :param in_dat_dict:
    :return:
    """
    for index, item in enumerate(in_dat_dict):
        print item['photo_url']
        req = requests.get(item['photo_url'], stream=True)
        fname = join(IMAGEDIR, str(index) + "_img.png")
        with open(fname, 'wb') as stream_file:
            for chunk in req.iter_content():
                stream_file.write(chunk)


def parse_image_data_file(in_fname):
    """
    parse a custom-formatted file into a dict and return those values for joining
    :param in_fname:
    :return:
    """
    in_file = file(in_fname, 'r')

    ret_vals = dict()
    c_val = None
    for line in in_file:
        try:
            c_val = int(line.strip())
            ret_vals[c_val] = dict()
        except ValueError:
            objs = [_.strip() for _ in line.split(":")]
            ret_vals[c_val][objs[0]] = objs[1]
    return ret_vals

    in_file.close()


def scrape_to_json(f_out):
    """
    scrape data to a json file
    :return:
    """
    # pylint: disable=invalid-name
    contestant_data = list()
    for i in range(0, 28):
        tgt_file = join(PICKLEDIR, str(i) + ".pickle")
        contestant_data.append(individual_extract(tgt_file))

    joiners = parse_image_data_file(join(DATADIR, "image_data.dat"))

    hl_set = set()

    final_data = list()
    for i in range(0, len(joiners)):
        final_data.append(dict(joiners[i].items() + contestant_data[i].items()))
        hl_set.add(joiners[i]['ethnicity'])

    print hl_set

    # json_out = file(f_out, 'w')
    # json_out.write(json.dumps(final_data, indent=4, separators=(',', ': ')))
    # json_out.close()


if __name__ == '__main__':
    scrape_to_json("contestants_27jan2015.json")


