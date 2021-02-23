from django.urls import path

from task.views import *

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path('article/<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
    path('notes/', NoteListView.as_view(), name="note_list"),
    path('note/add/', NoteCreate.as_view(), name="note_create"),
    path('note/<slug:slug>/', NoteDetailView.as_view(), name='note_detail'),
    path('note/<slug:slug>/update/', NoteUpdate.as_view(), name='note_update'),
    path('note/<slug:slug>/delete/', NoteDelete.as_view(), name='note_delete'),
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('task/add/', TaskCreateView.as_view(), name='task_create'),
    path('task/<slug:slug>/', TaskDetailView.as_view(), name='task_detail'),
    path('task/<slug:slug>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('task/<slug:slug>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    path('login/', UserLoginView.as_view(), name='login_page'),
    path('register/', RegisterUserView.as_view(), name='register_page'),
    path('logout/', UserLogoutView.as_view(), name='logout_page'),
    path('calendar/', CalendarView.as_view(), name='calendar'),

]
