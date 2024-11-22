from django.contrib import admin
from django.urls import path
from kanban.views import CurrentUserViewSet, LoginView, RegisterView, TasksViewSet, UsersViewSet, ContactsViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', LoginView.as_view()),
    path('api/register/', RegisterView.as_view()),
    path('api/tasks/', TasksViewSet.as_view()),
    path('api/tasks/<int:pk>/', TasksViewSet.as_view()),
    path('api/users/', UsersViewSet.as_view()),
    path('api/users/<int:pk>/', UsersViewSet.as_view()),
    path('api/currentuser/', CurrentUserViewSet.as_view()),
    path('api/contacts/', ContactsViewSet.as_view()),
    path('api/contacts/<int:pk>/', ContactsViewSet.as_view()),
]
