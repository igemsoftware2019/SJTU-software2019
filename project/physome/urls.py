from django.urls import path
from physome import views
urlpatterns = [
    path('',views.index,name='index'),
    path('partdata/',views.partdata,name='partdata'),
    path('metadata/',views.metadata,name='metadata'),
    path('prediction/',views.prediction,name='prediction'),
    path('help/',views.help,name='help'),
]