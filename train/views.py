from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

import numpy as np

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

import json

from .base import NueralNetWeb,tokenize,stem,bag_of_words

def loadCustomerJSON():
  with open('cust_intents.json', 'r') as f:
      return json.load(f)

def loadAuthJSON():
  with open('auth_intents.json', 'r') as f:
    return json.load(f)

def loadAdminJSON():
  with open('admin_intents.json','r') as f:
    return json.load(f)


@api_view(['GET'])
def train(request):
  cust_intents = loadCustomerJSON()
  auth_intents = loadAuthJSON()
  admin_intents = loadAdminJSON()
  intents_dict = {"cust_data":cust_intents,"auth_data":auth_intents,"admin_data":admin_intents}
  for key in intents_dict:
    intents = intents_dict[key]
    all_words = []
    tags = []
    xy = []

    for intent in intents['intents']:
      tag = intent['tag']
      tags.append(tag)
      for pattern in intent['patterns']:
          w = tokenize(pattern)
          all_words.extend(w)
          xy.append((w, tag))

    ignore_words = ['?', '.', '!']

    stemmed_unique_words = [stem(w) for w in all_words if w not in ignore_words]
    stemmed_unique_words = sorted(set(stemmed_unique_words))
    tags=sorted(tags)

    X_train = []
    y_train = []

    for (pattern_sentence, tag) in xy:
        bag = bag_of_words(pattern_sentence, stemmed_unique_words)
        X_train.append(bag)
        label = tags.index(tag)
        y_train.append(label)

    X_train = np.array(X_train)
    y_train = np.array(y_train)
    print("Xtrain",X_train.shape,y_train.shape)
    input_size  = len(X_train[0])
    output_size = len(tags) 
    hidden_size = 8
    num_epochs = 1000
    batch_size = 8
    learning_rate = 0.001

    class WebDataset(Dataset):

      def __init__(self):
        self.n_samples  = len(X_train)
        self.x_data     = X_train
        self.y_data     = y_train

      def __getitem__(self,index):
        return self.x_data[index],self.y_data[index]

      def __len__(self):
        return self.n_samples

    dataset = WebDataset()
    train_loader = DataLoader(dataset=dataset,
                              batch_size=batch_size,
                              shuffle=True,
                              num_workers=0)


    basic_model = NueralNetWeb(input_size,hidden_size,output_size)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(basic_model.parameters(),lr=learning_rate)

    for epoch in range(num_epochs):
        for (words,labels) in train_loader:
            outputs = basic_model(words)
            loss =criterion(outputs,labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        if (epoch+1) % 100 == 0:
            print (f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

    print(f'final loss: {loss.item():.4f}')
    print(f"Training COmplete - {key}")
    
    basic_model_data = {
    "model_state": basic_model.state_dict(),
    "input_size": input_size,
    "hidden_size": hidden_size,
    "output_size": output_size,
    "stemmed_unique_words": stemmed_unique_words,
    "tags": tags
    }
    print(tags)
    filename = key+'.pth'
    FILE = filename
    torch.save(basic_model_data, FILE)
    print(f'Training complete. File saved to {FILE}')
  return Response({'Bot':'Training complete. File saved'})

