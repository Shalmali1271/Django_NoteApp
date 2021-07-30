from django.urls import path
from .views import NoteList, NoteDetail, CreateNote, UpdateNote, DeleteNote, UserLogin, RegisterPage
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('login/', UserLogin.as_view(), name = "login"),
    path('logout/', LogoutView.as_view(next_page = 'login'), name = "logout"),
    path('register/', RegisterPage.as_view(), name = "register"),
    path('', NoteList.as_view(), name = "notes"), 
    path('note/<int:pk>/', NoteDetail.as_view(), name = "note"), 
    path('create-note/', CreateNote.as_view(), name = "create-note"), 
    path('update-note/<int:pk>/', UpdateNote.as_view(), name = "update-note"),
    path('delete-note/<int:pk>/', DeleteNote.as_view(), name = "delete-note"),
]