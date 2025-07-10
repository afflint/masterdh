from tqdm import tqdm

from vatican.data import VaticanCorpus
from vatican.indexing import VaticanIndexing
import spacy

nlp = spacy.load("it_core_news_lg")
folder = '/Users/flint/Data/vatican/data'

corpus = VaticanCorpus(folder=folder)
index = VaticanIndexing(corpus=corpus, dbname='vatican', language=nlp)

document_list = []
for pope in corpus.popes:
    for document, date in corpus.pope_documents(pope):
        document_list.append((pope, document))

for pope, document in tqdm(document_list):
    tokens = [x for x in index.tokenize_document(pope, document)]
    index.store_document(pope, document)