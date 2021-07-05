from django.urls import path

from core.state_runner import views

__author__ = 'Shekhar Upadhaya'

urlpatterns = [
    path('upload_session', views.session_uploader, name='upload_session'),
    path('update_session_graph', views.update_session_graph, name='update_session_graph')
]