from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.FileUploadView.as_view(), name='file-upload'),
    path('list/', views.FileListView.as_view(), name='file-list'),
    path('download/<str:token>/', views.FileDownloadView.as_view(), name='download'),

]