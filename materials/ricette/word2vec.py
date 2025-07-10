import pandas as pd 
import numpy as np 
import spacy 
from nltk.tokenize import word_tokenize

file_path = "/Users/flint/Data/recipe/italian/gz_recipe.csv"
R = pd.read_csv(filepath_or_buffer=file_path, index_col=0)


ingredient_collection = []
for i in R['Ingredienti'].values:
    first = i.split('], [')
    ingredients = []
    for word in first:
        ingredients.append(word.split('", "')[0].split("', '")[0].lstrip("[").lstrip("'"))
    ingredient_collection.append(ingredients)
    
corpus = []
categories = R['Categoria']
titles = R['Nome']
steps = R['Steps']
for i, title in enumerate(titles):
    s = steps[i]
    if pd.isnull(s):
        s = ""
    ingr = ", ".join(ingredient_collection[i])
    text = "\n".join([title, ingr, s])
    corpus.append(text)
    

tokenized_corpus = [word_tokenize(x.lower()) for x in corpus]

print(tokenized_corpus[0])    

# Word2Vec
from gensim.models import Word2Vec


model = Word2Vec(sentences=tokenized_corpus, vector_size=50, window=6, 
                min_count=4, workers=4, epochs=25)
model.save("word2vec.model")
    
