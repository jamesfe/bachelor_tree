# coding: utf-8
"""
A data gathering workflow for The Bachelor
"""
from __future__ import (absolute_import, division, print_function, unicode_literals)

# from os.path import join
from .season import Season
# import requests


PICKLEDIR = "../pickles/"
IMAGEDIR = "../images/"
DATADIR = "../data/"

CURR_SEASON_CODE = "cast/11-"
SITE_URL = "http://abc.go.com/shows/the-bachelorette"

##### TODO: Fix this commented code - quite contrary to the clean code principles. (JF, 26 May 2015)
# def gather_all_pages_to_pickle():
#     links = get_main_links()
#     for index, link in enumerate(links):
#         newfile = join(PICKLEDIR, str(index) + ".pickle")
#         pickle_indiv_pages(link, newfile)
#
#
# def download_images(in_dat_dict):
#     """
#     takes a data dict from individual_extract() and downloads the images to a folder
#     :param in_dat_dict:
#     :return:
#     """
#     for index, item in enumerate(in_dat_dict):
#         print(item['photo_url'])
#         req = requests.get(item['photo_url'], stream=True)
#         fname = join(IMAGEDIR, str(index) + "_img.png")
#         with open(fname, 'wb') as stream_file:
#             for chunk in req.iter_content():
#                 stream_file.write(chunk)
#
#
# def parse_image_data_file(in_fname):
#     """
#     parse a custom-formatted file into a dict and return those values for joining
#     :param in_fname:
#     :return:
#     """
#     in_file = open(in_fname, 'r')
#
#     ret_vals = dict()
#     c_val = None
#     for line in in_file:
#         try:
#             c_val = int(line.strip())
#             ret_vals[c_val] = dict()
#         except ValueError:
#             objs = [_.strip() for _ in line.split(":")]
#             ret_vals[c_val][objs[0]] = objs[1]
#
#     in_file.close()
#     return ret_vals


if __name__ == '__main__':
    Season(CURR_SEASON_CODE, SITE_URL)


