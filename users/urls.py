from django.urls import path

from . import views

urlpatterns = [
    # LOGIN LOGOUT
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    path('register/', views.registerPage, name="register"),
    # PROFILE VIEWING
    path('', views.profiles, name='profiles'),
    path('profile/<str:pk>/', views.userProfile, name="profile"),
    # PROFILE EDITING
    path('account/', views.userAccount, name="account"),
    path('edit-account/', views.editAccount, name="edit-account"),
    # INTEREST EDITING
    path('create-interest/', views.createInterest, name="create-interest"),
    path('update-interest/<str:pk>/',
         views.updateInterest, name="update-interest"),
    path('delete-interest/<str:pk>/',
         views.deleteInterest, name="delete-interest"),
    # MESSAGE SENDING
    path('inbox/', views.inbox, name="inbox"),
    path('message/<str:pk>/', views.viewMessage, name="message"),
    path('create-message/<str:pk>/', views.createMessage, name="create-message")
]
