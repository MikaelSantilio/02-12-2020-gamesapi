"""
Book: Building RESTful Python Web Services
Chapter 2: Working with class based views and hyperlinked APIs in Django
Author: Gaston C. Hillar - Twitter.com/gastonhillar
Publisher: Packt Publishing Ltd. - http://www.packtpub.com
"""
from django.urls import path
from games import views

urlpatterns = [
 # descomentar as linhas abaixo quando as funções forem implementadas
   path('games/', views.game_list),
   path('games/<int:pk>/', views.game_detail),
]
