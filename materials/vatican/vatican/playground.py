import platform
from vatican.data import VaticanCorpus

import spacy

nlp = spacy.load("it_core_news_lg")


print("Test Vatican Project with Python {}.{}.{}".format(*platform.python_version_tuple()))

folder = '/Users/flint/Data/vatican/data'

corpus = VaticanCorpus(folder=folder)

print("\n=================\n")

print(corpus.popes)

search_pope = 'Paul VI'
print("\nDocuments from {}".format(search_pope))
for doc, date in sorted(corpus.pope_documents(search_pope)):
    print(date, doc)

print(corpus.get_text(search_pope, 'Humanae Vitae'))

print("\n=================\n")
