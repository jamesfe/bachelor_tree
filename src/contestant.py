import json
# from bs4 import BeautifulSoup
from selenium import webdriver


class Contestant(object):

    def __init__(self):
        self.raw_content = None
        self.url = None

    def save_to_pickle(self):
        pass

    def collect_from_url(self, url):
        browser = webdriver.Firefox()

        browser.get(url)
        self.raw_content = browser.page_source
        self.url = url
        browser.quit()

    def set_attributes(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def load_from_pickle(self, filename):
        with open(filename, 'rb') as ofile:
            self.set_attributes(json.loads(ofile.read()))

    def to_quantifiable(self):
        pass
        ##### TODO: Fix this commented code - quite contrary to the clean code principles. (JF, 26 May 2015)
        # ret_vals = dict()
        #
        # data_soup = BeautifulSoup(self.raw_content['content'])
        # descript = data_soup.find("div", class_='descriptionBody')
        # status = data_soup.find("h2", class_='itemMeta').text.split(" - ")
        # if len(status) == 2:
        #     ret_vals['eliminated'] = True
        #     ret_vals['goneweek'] = int(status[1].strip()[-1:])
        # else:
        #     ret_vals['eliminated'] = False
        #
        # name = data_soup.find("h1", class_='title').text
        # ret_vals['name'] = name.strip()
        #
        # prof_photo = data_soup.find("div", class_="imageContainer").find("img")
        # ret_vals['photo_url'] = prof_photo['src']
        #
        # item_list = str(descript).split("<br/>")
        # ret_vals['age'] = int(item_list[0].strip()[-2:])
        #
        # occ_html = BeautifulSoup(item_list[1])
        # ret_vals['occupation'] = occ_html.text.split(":")[1].strip()
        #
        # hometown_html = BeautifulSoup(item_list[2])
        # hometown = hometown_html.text.split(":")[1].strip().split(",")
        # ret_vals['hometown_name'] = hometown[0]
        # try:
        #     ret_vals['hometown_state'] = hometown[1]
        # except IndexError:
        #     ret_vals['hometown_state'] = 'UNK'
        #
        # height = BeautifulSoup(item_list[3]).text.split(":")[1].replace('"', '').split("'")
        # height_inches = int(height[0]) * 12 + int(height[1])
        # ret_vals['height_inches'] = height_inches
        #
        # txt_num_tats = BeautifulSoup(item_list[4]).text.split(":")[1].strip()
        #
        # try:
        #     num_tats = int(txt_num_tats)
        # except ValueError:
        #     num_tats = self.convert_text_to_num(txt_num_tats)
        #
        # ret_vals['num_tattoos'] = num_tats
        #
        # likes = BeautifulSoup(item_list[5]).text.split(":")[1].split(",")
        # ret_vals['likes'] = [str(_).strip() for _ in likes]
        #
        # datefear = BeautifulSoup(item_list[6]).text.split(":")[1]
        # ret_vals['date_fear'] = datefear
        #
        # ret_vals['free_text'] = BeautifulSoup(' '.join(item_list[7:])).text
        #
        # return ret_vals

    @staticmethod
    def convert_text_to_num(input_string):
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
            ret_val = conversion[input_string.strip().lower()]
        except KeyError:
            ret_val = -1
        return ret_val