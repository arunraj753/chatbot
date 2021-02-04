from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .models import Inquiry,Career,ResetCode
from .extra_cust import get_business_details
from datetime import datetime
from subscribe.views import ResetMail
import random

def Guest_PreChecks(request,sentence):

  user_interest = request.session.get('user_interest',False)
  user_details  = request.session.get('user_details',False)
  user_id = (request.session.get('user_id',False))
  user_chance = int(request.session.get('user_chance',0))
  user_name = (request.session.get('user_name',False))
  business_details = request.session.get('business_details',False)
  # session storage variables for employer
  loginChance  = request.session.get('loginChance',0)
  loginUsername = request.session.get('loginUsername',False)
  #
  pass_reset = request.session.get('pass_reset',False)
  code_accept =request.session.get('code_accept',False)
  reply_dict = {}

  session_keys = list(request.session.keys())
  
  if code_accept:
    return {"Bot":"Sorry. Feature not available at the moment!"}

  if int(loginChance)>0:
    reply_dict = LoginProcedures(request,sentence,loginUsername)
    return reply_dict
  if user_interest:
    
    if user_details and not business_details:

      reply_dict = get_business_details(request,user_id,sentence)
      return reply_dict
    elif not user_details:
      if not user_id and user_chance>0:
        try:
          validate_email(sentence)
          new_inquiry = Inquiry()
          new_inquiry.email=sentence
          new_inquiry.save()
          request.session['user_id']=new_inquiry.pk
          reply_dict.update({'Bot':"How may I address you ?"})  
          request.session['user_chance']=2
          return reply_dict
        except ValidationError as e:
          msg = str(e.message)
          reply_dict.update({'Bot_': msg})
          request.session['user_chance'] = user_chance-1
          return reply_dict
      elif user_id  and (not user_name) and (user_chance >0):
        inq = Inquiry.objects.get(pk=int(user_id))
        inq.name = sentence
        inq.save()
        request.session['user_name'] = True
        reply_dict.update({'Bot':"Can I get your contact number ?"})  
        return reply_dict
      elif (user_id) and (user_name) and user_chance>0:
        request.session['user_chance'] = user_chance-1
        try:
          if len(sentence) == 10 :    
            num = int(sentence)
            inq = Inquiry.objects.get(pk=int(user_id))
            inq.mobile = num
            inq.save()
            request.session['user_chance'] = 0     
            request.session['user_details'] = True
            reply_dict.update({'Bot': 'What kind of website you are looking for ? '})
            webList = ['Ecommerce','Blog','Educational','Entertainment','Web Application','Portfolio']
            reply_dict.update({"Bot_C":webList})
            return reply_dict
          else:
            reply_dict.update({'Bot_': 'Enter a valid number'})
            return reply_dict
        except:
          reply_dict.update({'Bot_': 'Enter a valid number'})
          return reply_dict
  return reply_dict
def Jobs(request):
  careers = Career.objects.filter(job_status=False)
  jobsList = []
  for career in careers:
    job =f"{career.title} - {career.vaccany}"
    jobsList.append(job)
  reply_dict={}
  if careers:
    reply_dict.update({"Bot":"Yes Jobs are availabe at https://www.weinsoft.in/careers"})
    reply_dict.update({"Bot_L":jobsList})

  else:
    reply_dict.update({"Bot":"Sorry. No open positions at the moment "})
  return reply_dict



def LoginProcedures(request,sentence,loginUsername):
    loginChance = int(request.session["loginChance"])
    reply_dict={}
    if not loginUsername:
      user_obj = User.objects.filter(username=sentence)
      if user_obj:
        request.session['loginUsername'] = user_obj[0].username
        reply_dict.update({"Bot":"Enter your password"})
        return (reply_dict)
      else:
        
        request.session['loginChance'] = loginChance-1
        if loginChance == 1 :
          request.session['loginUsername']=False
          reply_dict.update({"Bot":"Username invalid"})
          reply_dict.update({"Bot_":"Exited Login Procedures..."})
          return (reply_dict)
        reply_dict.update({"Bot":"Enter a valid username"})
        return (reply_dict)
    else:
      user = authenticate(request,username=loginUsername, password=sentence)
      if user is not None:
        login(request,user)
        reply_dict.update({"Bot":"Login Success. Please refresh the webpage"})
        
        request.session['loginChance']=loginChance-1
        request.session['loginUsername']=False
        return (reply_dict)
      else:
        request.session['loginChance']=loginChance-1
        request.session['loginUsername']=False
        reply_dict.update({"Bot":"Authentication Failed"})
        reply_dict.update({"Bot_":"Exiting Login Procedures..."})
        return (reply_dict)

def Help(request):
  common = ["Where are you ?","Who are you","About company?","Available Jobs","I need a service"]
  reply_dict={}
  reply_dict.update({'Bot_C':common})
  return reply_dict
def CustomerTags(request,tag):
  if tag == "enquiry":
      message ={}
      message.update({'Bot_':'Interested in working with us on a project?'})
      message.update({"Bot_Q":["Later","Sure"]})
      return message
  elif tag == "interested":
    #user_interest =request.session['user_interest']
  #   session_keys = list(request.session.keys())
  #   for key in session_keys:
  #     print (key)
  #  # print("user detaisls",request.session.get('user_details'))
    user_details  = request.session.get('user_details',False)
    if not user_details:
    #if not user_interest:
      request.session['user_interest'] = True
      request.session['user_chance']=1
      return None
    elif user_details == True:
      reply_dict={}
      reply_dict.update({"Bot":"Great. Here is the link"})
      reply_dict.update({"Bot__":"https://www.weinsoft.in/portfolio"})
      return (reply_dict)
  elif tag == 'goodbye':
    session_keys = list(request.session.keys())
    for key in session_keys:
        del request.session[key]
        print(key)
    message = ({'Bot_':'Chat session cleared'})
    print("Chat session cleared")
    return message
  elif tag == 'login':
    request.session['loginChance'] =1
    return None

  elif tag == 'career':
    print("here")
    return Jobs(request)
  
  elif tag == 'help':
    print("Help tag in utilities")
    return Help(request)
  elif tag == 'reset':
    return {"Bot":"Sorry. Feature not available at the moment!"}

  
 
