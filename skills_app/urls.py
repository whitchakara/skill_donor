from django.urls import path     
from . import views

urlpatterns = [ 
    path('', views.index),
    path('register',views.register),
    path('login', views.login),
    path('dashboard', views.dashboard),
    # path('skill/<int:skill_id>', views.one_skill),
    # path('create',views.create),
    # path('update/<int:skill_id>', views.update),
    # path('delete/<int:skill_id>', views.delete),
    # path('user/<int:id>', views.profile),
    # path('logout', views.logout),
]