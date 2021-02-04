from django.shortcuts import render
from chat.models import Inquiry

def dashboard(request):
  inq = Inquiry.objects.all()
  context = {'inquires':inq}
  return render(request,"dashboard/dashboard.html",context)
