import pymongo
from spacy.language import Language

from vatican.data import VaticanCorpus


class VaticanIndexing(object):
    def __init__(self,
                 corpus: VaticanCorpus,
                 dbname: str,
                 language: Language
                 ):
        self.db = pymongo.MongoClient()[dbname]
        self.corpus = corpus
        self.nlp = language
        self.tokens_collection = self.db['tokens']

    def tokenize_document(self, pope: str, document: str):
        text = self.corpus.get_text(pope, document)
        doc = self.nlp(text)
        date = self.corpus.get_date(pope, document)
        for i, sentence in enumerate(doc.sents):
            for token in sentence:
                token_data = {
                    'pope': pope,
                    'document': document,
                    'sentence': i,
                    'date': date,
                    'idx': token.idx,
                    'text': token.text,
                    'lemma': token.lemma_,
                    'pos': token.pos_,
                    'dep': token.dep_
                }
                yield token_data

    def store_document(self, pope: str, document: str):
        tokens = [x for x in self.tokenize_document(pope, document)]
        self.tokens_collection.insert_many(tokens)
