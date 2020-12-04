from django.conf.urls import  include, path

urlpatterns = [
   path('', include('games.urls'))
]