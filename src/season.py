from bs4 import BeautifulSoup
import json
import requests

from .contestant import Contestant


class Season(object):

    def __init__(self, season_code, site_url):
        self.season_code = season_code
        self.site_url = site_url
        self.contestants = list()

    def export_to_dict(self):
        contestant_data = list()
        for contestant in self.contestants:
            contestant_data.append(contestant.to_quantifiable())
        return contestant_data

    def export_to_json(self):
        return json.dumps(self.export_to_dict(), indent=4, separators=(',', ': '))

    def build_contestants_from_web(self):
        main_data = requests.get(self.site_url)
        bs_text = BeautifulSoup(main_data.text)
        profiles = bs_text.find_all('a', class_='imageContainer')

        for profile in profiles:
            cast_link = profile['href']
            if cast_link.find(self.season_code) > -1:
                new_contestant = Contestant()
                new_contestant.url = profile['href']
            self.contestants.append(new_contestant)
