from django.contrib.auth.models import User
from django.contrib.auth import logout
from .models import LeaveApplication,Leave,Project,News
from datetime import datetime,date
from django.core.mail import send_mail
from datetime import date

def Employer_PreChecks(request,sentence):
  print('Employer prechecks')
  reply_dict={}
  empLeave = request.session.get('empLeave',False)
  eod_request = request.session.get('eod_request',False)
  print(empLeave )
  if empLeave:
    request.session['empLeave'] = False
    reply_dict = LeaveProcedures(request,sentence)
    return reply_dict
  elif eod_request:
    reply_dict = EodContents(request,sentence)
    return reply_dict
  return reply_dict
  
def CheckForLeave(request):
  leave_object = Leave.objects.get(user=request.user)
  if leave_object.available>0:
    request.session['empLeave'] = True
    print("Leave status is ",request.session.get('EmpLeave'))
    return {"Bot_":"When you need an off ?"}
    
  else:
    return ({"Bot_":"Sorry You dont have any Casual Leaves available."})

def LeaveProcedures(request,sentence):
  try:
    print(sentence)
    date_format = "%d/%m/%Y"
    date = datetime.strptime(sentence,date_format).date()
    leave = LeaveApplication()
    leave.user = request.user
    leave.date = date
    leave.save()
    leave_date = date.strftime("%b %d %Y")
    return ({"Bot":f"Leave Applied for {leave_date} !"})
  except:
    return ({"Bot":"Leave application error"})

def LeaveStatus(request):
  leave_object = LeaveApplication.objects.filter(user=request.user).last()
  print(leave_object,leave_object.status)
  if leave_object and leave_object.date > date.today():
    leave_date = leave_object.date.strftime("%b %d %Y")
    if leave_object.status == True:
      return ({"Bot":f"Admin has approved your leave request for {leave_date} !"})
    elif leave_object.status == False:
      return ({"Bot":f"Admin has rejected your leave request for {leave_date} !"})
    else:
      return ({"Bot":"Pending for approval"})
  else:
    return ({"Bot":"You haven't applied for any leaves !"})

def ProjectDetails(request):
  project_object = Project.objects.filter(user=request.user).last()
  if project_object:
    deadline = project_object.deadline.strftime("%b %d %Y")
    return ({"Bot":f"Your project is on {project_object.title}. Submission Date:{deadline}"})

def LatestNews(request):
  latest = News.objects.last()
  if latest:
    post_date = latest.date.strftime("%b-%d")
    return({"Bot":f"{post_date}.  Admin : {latest.news}. "})

def Logout(request):
  try:
    logout(request)
    return({"Bot":"Logout \n Success !"})
  except:
    return({"Bot":"Error- Failed to Logout"})

def EmployerTags(request,tag):

  if tag == 'leave':
    return CheckForLeave(request)
  
  elif tag == 'leave_status':
    return LeaveStatus(request)
  
  elif tag == 'project':
    return ProjectDetails(request)
  
  elif tag == 'updates':
    return LatestNews(request)

  elif tag == 'logout':
    return Logout(request)

  elif tag == 'EOD':
    return {"Bot":"Sorry. Feature not available at the moment!"}