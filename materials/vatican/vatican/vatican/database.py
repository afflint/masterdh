from typing import List

import numpy as np
import pandas as pd
import pymongo
from tqdm import tqdm


class VaticanMongoDb(object):

    def __init__(self, db_name: str, collection: str):
        self.db_name = db_name
        self.collection = collection
        self.db = pymongo.MongoClient()[self.db_name][self.collection]

    @property
    def popes(self):
        return self.db.distinct('pope')

    @property
    def documents(self) -> List[tuple]:
        q = {'$group': {'_id': {'pope': '$pope', 'document': '$document'}}}
        docs = []
        for record in self.db.aggregate([q]):
            docs.append((record['_id']['pope'], record['_id']['document']))
        return docs

    def document_term_count(self, pope, document, field='lemma'):
        m = {'$match': {'pope': pope, 'document': document}}
        g = {'$group': {'_id': "${}".format(field), 'count': {'$sum': 1}}}
        data = {}
        for record in self.db.aggregate([m, g]):
            data[record['_id']] = record['count']
        return pd.Series(data)

    def pope_term_count(self, pope, field='lemma', normalized: bool = False):
        m = {'$match': {'pope': pope}}
        g = {'$group': {'_id': "${}".format(field), 'count': {'$sum': 1}}}
        data = {}
        for record in self.db.aggregate([m, g]):
            data[record['_id']] = record['count']
        freq = pd.Series(data)
        if normalized:
            freq = freq / freq.sum()
        return freq

    def sentence_df(self, field='lemma'):
        g = {'$group': {'_id': {'token': "${}".format(field),
                                'document': "$document", 'sentence': "$sentence"}}}
        g2 = {'$group': {'_id': '$_id.token', 'count': {'$sum': 1}}}
        data = {}
        for record in self.db.aggregate([g, g2], allowDiskUse=True):
            data[record['_id']] = record['count']
        return pd.Series(data)

    @property
    def sentence_count(self):
        g = {'$group': {'_id': {'document': "$document", 'sentence': "$sentence"}}}
        return len([x for x in self.db.aggregate([g])])

    def sentence_idf(self, field='lemma'):
        return np.log(self.sentence_count / self.sentence_df(field=field))

    @staticmethod
    def generate_filter(pope, document):
        return {'$match': {'pope': pope, 'document': document}}

    def term_count(self, field: str = 'lemma', m: dict = None, normalized: bool = False):
        g = {'$group': {'_id': "${}".format(field), 'count': {'$sum': 1}}}
        data = {}
        if m is None:
            pipeline = [g]
        else:
            pipeline = [m, g]
        for record in self.db.aggregate(pipeline):
            data[record['_id']] = record['count']
        freq = pd.Series(data)
        if normalized:
            freq = freq / freq.sum()
        return freq

    def get_sentences(self, pope: str, document: str, field='lemma'):
        q = {'$group': {'_id': {'pope': '${}'.format(pope),
                                'document': '${}'.format(document),
                                'sentence': '$sentence'},
                        'tokens': {'$push': {'sentence': '$sentence',
                                             'token': '${}'.format(field),
                                             'idx': '$idx',
                                             'pos': '$pos'
                                             }}}}
        docs = []
        for record in self.db.aggregate([q], allowDiskUse=True):
            docs.append(record['tokens'])
        return docs

    def get_sentence_corpus(self, field='lemma'):
        documents = []
        for pope, document in tqdm(self.documents):
            for sentence in self.get_sentences(pope, document, field=field):
                documents.append(VaticanMongoDb.to_words(sentence))
        return documents

    def get_pope_corpus(self, pope_query: str, field: str = 'lemma'):
        documents = []
        for pope, document in tqdm(self.documents):
            if pope == pope_query:
                for sentence in self.get_sentences(pope, document, field=field):
                    documents.append(VaticanMongoDb.to_words(sentence))
        return documents

    @staticmethod
    def to_words(sentence):
        return [x['token'] for x in sorted(sentence, key=lambda w: w['idx'])]