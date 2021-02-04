from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.decorators import api_view,permission_classes
from django.shortcuts import render
import numpy as np
import random
import json
from .models import Inquiry

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from .base import NueralNetWeb,tokenize,stem,bag_of_words
from .utilities import (Guest_PreChecks,LoginProcedures,CustomerTags)
from .emp_utilities import Employer_PreChecks,EmployerTags
from .admin_utilities import Admin_PreChecks,AdminTags

import re

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

with open('cust_intents.json', 'r') as f:
  cust_intents = json.load(f)
with open('auth_intents.json', 'r') as f:
  auth_intents = json.load(f)
with open('admin_intents.json', 'r') as f:
  admin_intents = json.load(f)

CUST_FILE = "cust_data.pth"
AUTH_FILE = "auth_data.pth"
ADMIN_FILE='admin_data.pth'

cust_model_data = torch.load(CUST_FILE)
cust_input_size  = cust_model_data["input_size"]
cust_hidden_size = cust_model_data["hidden_size"]
cust_output_size = cust_model_data["output_size"]
cust_stemmed_unique_words = cust_model_data['stemmed_unique_words']
cust_tags        = cust_model_data['tags']
cust_model_state = cust_model_data["model_state"]
cust_model = NueralNetWeb(cust_input_size, cust_hidden_size, cust_output_size)
cust_model.load_state_dict(cust_model_state)
cust_model.eval()

auth_model_data = torch.load(AUTH_FILE)
auth_input_size  = auth_model_data["input_size"]
auth_hidden_size = auth_model_data["hidden_size"]
auth_output_size = auth_model_data["output_size"]
auth_stemmed_unique_words = auth_model_data['stemmed_unique_words']
auth_tags        = auth_model_data['tags']
auth_model_state = auth_model_data["model_state"]
auth_model = NueralNetWeb(auth_input_size, auth_hidden_size, auth_output_size)
auth_model.load_state_dict(auth_model_state)
auth_model.eval()

admin_model_data = torch.load(ADMIN_FILE)
admin_input_size  = admin_model_data["input_size"]
admin_hidden_size = admin_model_data["hidden_size"]
admin_output_size = admin_model_data["output_size"]
admin_stemmed_unique_words = admin_model_data['stemmed_unique_words']
admin_tags        = admin_model_data['tags']
admin_model_state = admin_model_data["model_state"]
admin_model = NueralNetWeb(admin_input_size, admin_hidden_size, admin_output_size)
admin_model.load_state_dict(admin_model_state)
admin_model.eval()

@api_view(['GET'])
def home(request):
  return render (request,'chat/home.html')
  
def ModelSelection(request):
  global auth_model,auth_stemmed_unique_words,auth_tags,auth_intents,cust_model,cust_stemmed_unique_words,cust_tags,cust_intents,admin_model,admin_stemmed_unique_words,admin_tags,admin_intents

  if request.user.is_authenticated:
    if request.user.is_superuser:
      return admin_intents,admin_model,admin_stemmed_unique_words,admin_tags,
    return auth_intents,auth_model,auth_stemmed_unique_words,auth_tags
  else:
    return cust_intents,cust_model,cust_stemmed_unique_words,cust_tags

@api_view(['POST'])
def chat(request):
  sentence = request.POST['text']
  reply_dict = {}
  intents,model,stemmed_unique_words,tags = ModelSelection(request)
  if not request.user.is_authenticated:
    reply_dict = Guest_PreChecks(request,sentence)
    UserTags = CustomerTags
    if 'Bot' in reply_dict:
      return Response(reply_dict)
  elif request.user.is_superuser:
    UserTags = AdminTags
    reply_dict = Admin_PreChecks(request,sentence)
    if 'Bot' in reply_dict:
      return Response(reply_dict)
  else:
    UserTags = EmployerTags
    reply_dict = Employer_PreChecks(request,sentence)
    if 'Bot' in reply_dict:
      return Response(reply_dict)

  
  sentence = tokenize(sentence)
  
  X = bag_of_words(sentence, stemmed_unique_words)

  X = X.reshape(1, X.shape[0])
  X = torch.from_numpy(X)
  output = model(X)

  _, predicted = torch.max(output, dim=1)

  tag = tags[predicted.item()]
  probs = torch.softmax(output, dim=1)
  prob = probs[0][predicted.item()]

  if prob.item() > 0.75:
    for intent in intents['intents']:
        if tag == intent["tag"]:
 
            reply = random.choice(intent['responses'])
            reply_dict.update({'Bot':reply})
            
    
    reply = UserTags(request,tag)

    if reply:
      reply_dict.update(reply)

  else:     
    reply_dict.update({'Bot':"Sorry,I didn't get you..."})  

  return Response(reply_dict)

def web(request):
  return render(request,"chat/messenger.html")

@api_view(['GET'])
def update(request):
  global cust_model_data,cust_input_size,cust_hidden_size,cust_output_size,cust_stemmed_unique_words,cust_tags,cust_model_state,cust_model,auth_model_data,auth_input_size,auth_hidden_size,auth_output_size,auth_stemmed_unique_words,auth_tags,auth_model_state,auth_model,admin_model_data,admin_input_size,admin_hidden_size,admin_output_size,admin_stemmed_unique_words,admin_tags,admin_model_state,admin_model

  CUST_FILE = "cust_data.pth"
  AUTH_FILE = "auth_data.pth"
  ADMIN_FILE="admin_data.pth"

  cust_model_data = torch.load(CUST_FILE)

  cust_input_size  = cust_model_data["input_size"]
  cust_hidden_size = cust_model_data["hidden_size"]
  cust_output_size = cust_model_data["output_size"]
  cust_stemmed_unique_words = cust_model_data['stemmed_unique_words']
  cust_tags        = cust_model_data['tags']
  cust_model_state = cust_model_data["model_state"]
  cust_model = NueralNetWeb(cust_input_size, cust_hidden_size, cust_output_size)
  cust_model.load_state_dict(cust_model_state)
  cust_model.eval()

  auth_model_data = torch.load(AUTH_FILE)
  auth_input_size  = auth_model_data["input_size"]
  auth_hidden_size = auth_model_data["hidden_size"]
  auth_output_size = auth_model_data["output_size"]
  auth_stemmed_unique_words = auth_model_data['stemmed_unique_words']
  auth_tags        = auth_model_data['tags']
  auth_model_state = auth_model_data["model_state"]
  auth_model = NueralNetWeb(auth_input_size, auth_hidden_size, auth_output_size)
  auth_model.load_state_dict(auth_model_state)
  auth_model.eval()

  admin_model_data = torch.load(ADMIN_FILE)
  admin_input_size  = admin_model_data["input_size"]
  admin_hidden_size = admin_model_data["hidden_size"]
  admin_output_size = admin_model_data["output_size"]
  admin_stemmed_unique_words = admin_model_data['stemmed_unique_words']
  admin_tags        = admin_model_data['tags']
  admin_model_state = admin_model_data["model_state"]
  admin_model = NueralNetWeb(admin_input_size, admin_hidden_size, admin_output_size)
  admin_model.load_state_dict(admin_model_state)
  admin_model.eval()

  return Response({"Bot":"Variables Updated"})


