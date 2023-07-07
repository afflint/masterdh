import os
import json
from datetime import datetime
from typing import List


class VaticanCorpus(object):

    def __init__(self, folder: str):
        self.data = {}
        self.dates = {}
        for pope in os.listdir(folder):
            self.data[pope] = {}
            self.dates[pope] = {}
            path = os.path.join(folder, pope, 'encyclicals')
            date_doc = os.path.join(folder, pope, "{}_pub_date.json".format(pope))
            with open(date_doc, 'r') as date_file:
                dates = json.load(date_file)
            for d_title, d_string in dates.items():
                self.dates[pope][d_title] = datetime.strptime(d_string, "%d/%m/%Y")
            for doc in os.listdir(path):
                subpath = os.path.join(path, doc, 'it', '{}.txt'.format(doc))
                with open(subpath, 'r') as infile:
                    content = infile.read()
                self.data[pope][doc] = content

    @property
    def popes(self) -> List[str]:
        return sorted(self.data.keys())

    def pope_documents(self, pope: str):
        try:
            for doc in self.data[pope].keys():
                yield doc, self.dates[pope][doc].date()
        except KeyError:
            raise KeyError('There are no documents for pope {}'.format(pope))

    def get_date(self, pope: str, document: str):
        try:
            return self.dates[pope][document]
        except KeyError:
            return None

    def get_text(self, pope: str, document: str):
        try:
            return self.data[pope][document]
        except KeyError:
            raise KeyError('There are no documents for pope {} and title {}'.format(
                pope, document))

