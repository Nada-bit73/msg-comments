from django.urls import path
from . import views
# urlpatterns => static name
urlpatterns = [
    # mapping '/' to index function in views file
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('view_wall', views.view_wall),
    path('logout', views.logout),    
    path('post_message', views.post_message),      
    path('post_comment', views.post_comment),    
    path('delete_comment/<int:commentId>', views.delete_comment),    
    path('delete_msg/<int:msgId>', views.delete_msg),    
]
#123@hHgj