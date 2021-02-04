# from django.core.validators import validate_email
# from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .models import Inquiry,Career,LeaveApplication,News,Project
from datetime import datetime
from django.core.validators import validate_email

def Add_Update(request,sentence):

  try :
    obj = News()
    obj.date = date.today()
    obj.news = sentence 
    obj.save()
    request.session['circular'] = False
    return ({"Bot":"Update Added!"})
  except:
    request.session['circular'] = False
    return ({"Bot":"An Error occured."})

def Add_Employee(request,sentence):
  request.session['addEmployee'] =False
  reply_dict={}
  u = User.objects.filter(email=sentence)
  if u:
    reply_dict.update({"Bot":"Account for the given email id already exists!"})
    reply_dict.update({"Bot_":"Exiting user creation procedures."})
    return reply_dict
  else:
    try:
      validate_email(sentence)
      user=User.objects.create_user(sentence,sentence,sentence+str(2021))
      reply_dict.update({'Bot':'Success!!.Login credentials are sent to '+sentence})
      return reply_dict
    except: 
      reply_dict.update({"Bot":"Error"})
      reply_dict.update({"Bot_":"Exiting user creation procedures."})
      return reply_dict

def Add_Project(request,sentence):
  reply_dict ={}
  def finished():
       request.session['addProject'] =False
       request.session['project_details'] =False
       request.session['emp_id'] =False
       
  
  emp_id   = request.session.get('emp_id',False)
  project_details = request.session.get('project_details',False)
  deadline = request.session.get('deadline',False)
  if not emp_id:
    try:
      u = User.objects.filter(username=sentence)
      request.session['emp_id'] = u[0].pk
      reply_dict.update({"Bot":"What are the project details ?"})
    except Exception as e:
      finished()
      reply_dict.update({"Bot":"Error. Exiting Add Project Procedures."})
  elif not project_details and (emp_id):
    emp_id = request.session['emp_id']
    project = Project()
    user = User.objects.get(pk=str(request.session['emp_id']))
    project.user = user
    project.title  =sentence
    project.save()
    reply_dict.update({"Bot":"Deadline in mm/dd/yyyy?"})
    request.session['project_details'] = True

  elif not deadline and (project_details):
    try:
      date_format = "%d/%m/%Y"
      date = datetime.strptime(sentence,date_format).date()
      print(date)
      user = User.objects.get(pk=str(request.session['emp_id']))
      project = Project.objects.filter(user=user).last()
      project.deadline =date
      project.save()
      reply_dict.update({"Bot":f"Project titled {project.title} is added to {user.username} with deadline on {date}"})
      
    except Exception as e:  
      print("Indate error loop")
      print(e)
      reply_dict.update({"Bot":"Error. Exiting Add Project Procedures."})
    finished()
  return reply_dict
    
def Admin_PreChecks(request,sentence):
  admin_circular = request.session.get('circular',False) 
  addEmployee    = request.session.get('addEmployee',False)
  leave_id       = request.session.get('leave_id',False)
  addProject     = request.session.get('addProject',False)

  reply_dict = {}
  if admin_circular:
    return Add_Update(request,sentence)
  elif addEmployee:
    return Add_Employee(request,sentence)
  elif addProject:
    return Add_Project(request,sentence)
  return reply_dict

def Logout(request):
  try:
    logout(request)
    return({"Bot":"Logout \n Success !"})
  except:
    return({"Bot":"Error- Failed to Logout"})

def Leaves(request):
  query = LeaveApplication.objects.filter(status=None).first()
  if query:
    reply_dict={}
    message = f"Leave applied by {query.user} for {query.date.strftime('%d  %b %Y')}"
    request.session['leave_id'] = query.pk
    reply_dict.update({"Bot":message})
    reply_dict.update({"Bot_Q":["Deny","Sanction"]})
    
    return reply_dict
  return {"Bot":"All requests updated!"}

def Help(request):
  common = ["New Requests","Add an update","Logout"]
  reply_dict={}
  reply_dict.update({'Bot_C':common})
  return reply_dict

def LeaveForward(request,status):
  if not request.session['leave_id']:
    return ({"Bot":"All requests are updated!!"})
  try:
    reply_dict = {}
    p_key = int(request.session['leave_id'])
    obj = LeaveApplication.objects.get(pk=p_key)
    obj.status = status
    obj.save()
    request.session['leave_id']=False
    reply_dict.update({"Bot_N":"Next Request"})
    
  except:
    reply_dict={"Bot":"An error occured"}
  return reply_dict

  
def EmployerList():
  email_list = []
  employers = User.objects.filter(is_superuser=False)
  for e in employers:
    email_list.append(e.username)
  return ({"Bot_C":email_list})

def AdminTags(request,tag):
  if tag == 'logout':
    return Logout(request)
  elif tag == 'leaves_applied':
    return Leaves(request)
  elif tag == 'announcement':
    request.session['circular'] = True
    return None
  elif tag == 'approve':
    return LeaveForward(request,status=True)
  elif tag == 'reject':
    return LeaveForward(request,status=False)
  elif tag == 'help':
    return Help(request)
  elif tag == 'addEmployee':
    request.session['addEmployee'] =True
    return None
  elif tag == 'addProject':
    request.session['addProject'] = True
    return EmployerList()
  return None
 
