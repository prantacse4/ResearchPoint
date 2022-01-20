from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('discussion/<str:pk>/', views.discussion, name="discussion"),
    path('create-discussion/', views.creatediscussion, name="create-discussion"),
    path('update-discussion/<str:pk>', views.updatediscussion, name="update-discussion"),
    path('delete-discussion/<str:pk>', views.deletediscussion, name="delete-discussion"),
    path('delete-comment/<str:pk>', views.deletecomment, name="delete-comment"),
    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),

    path('update-user/', views.updateUser, name="update-user"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

]
