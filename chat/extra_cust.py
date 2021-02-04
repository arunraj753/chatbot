from .models import Inquiry
def get_business_details(request,user_id,sentence):
  reply_dict={}
  business_details = request.session.get('business_details',False)
  platform= request.session.get('platform',False)
  budget = request.session.get('budget',False)
  business_type = request.session.get('business_type',False)
  print("In Business Details")
  try:
    if not business_type:
      app_type_list = ["I need a Web Application","I need a Mobile Application","I need both Web and Mobile Application"]
      inq = Inquiry.objects.get(pk=user_id)
      inq.business = sentence
      inq.save()
      request.session['business_type'] = True
      reply_dict.update({"Bot":"Great!. Well what kind of application yopu looking for ?"})
      reply_dict.update({"Bot_C":app_type_list})
    elif not platform:
      print("Platform is ",sentence)
      inq = Inquiry.objects.get(pk=user_id)
      inq.app_type=sentence
      inq.save()
      request.session['platform'] = True
      reply_dict.update({"Bot":"How much has been budgeted for this project"})
    
    elif not budget:
      inq = Inquiry.objects.get(pk=user_id)
      inq.budget=sentence
      inq.save()
      print("Budget is",sentence)
      reply_dict.update({'Bot': "Thank you for your interest. Our customer executive will contact you soon. Meanwhile you can take a look into our company's portfolio at "})
      reply_dict.update({"Bot__":"https://www.weinsoft.in/portfolio"})
      request.session['business_details'] = True
      request.session['user_interest']=True

  except Exception as e:
    print(e)
    reply_dict.update({"Message":"Error"})
  return reply_dict
