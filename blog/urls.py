from django.urls import path
from . import views

#namespace for your app
app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug_name>',views.post_detail,name="post_detail"),
]