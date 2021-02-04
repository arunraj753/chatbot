import torch
import torch.nn as nn
import numpy as np

import nltk
from nltk.stem.porter import PorterStemmer

stemmer = PorterStemmer()

class NueralNetWeb(nn.Module):

  def __init__(self,input_size,hidden_size,num_classes):
    super(NueralNetWeb,self).__init__()

    self.l1 = nn.Linear(input_size,hidden_size)
    self.l2 = nn.Linear(hidden_size,hidden_size)
    self.l3 = nn.Linear(hidden_size,num_classes)
    self.relu = nn.ReLU() 

  def forward(self,x):

    out = self.l1(x)
    out = self.relu(out)
    out = self.l2(out)
    out = self.relu(out)
    out = self.l3(out)
    return out

def tokenize(sentence):
    return nltk.word_tokenize(sentence)

def stem(word):
    return stemmer.stem(word.lower())

def bag_of_words(tokenized_sentence, words):
  
    sentence_words = [stem(word) for word in tokenized_sentence]
    bag = np.zeros(len(words), dtype=np.float32)
    for idx, w in enumerate(words):
        if w in sentence_words: 
            bag[idx] = 1
    return bag