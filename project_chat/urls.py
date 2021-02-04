from django.contrib import admin
from django.urls import path,include
from train import views as tviews
from dashboard import views as dviews
from django.conf import settings
from django.conf.urls.static import static
from subscribe import views as sviews 
urlpatterns = [
    path('',include('chat.urls')),
    path('admin/', admin.site.urls),
    path('train',tviews.train,name='model-train'),
    path('dashboard',dviews.dashboard,name='dashboard'),
    path('test-mail',sviews.TestEmail,name='test-email')    

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)