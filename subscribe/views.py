from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
@api_view(['GET'])
def TestEmail(request):
  return ({"Bot":"Sorry.Feature Not available at the moment!"})

def ResetMail(request,code=102030,email_ = 'arunraj753@gmail.com'):
  return True
  


