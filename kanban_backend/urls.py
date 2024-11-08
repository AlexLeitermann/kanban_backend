"""
URL configuration for kanban_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from kanban.views import CurrentUserViewSet, LoginView, RegisterView, TasksViewSet, UsersViewSet, ContactsViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include(router.urls)),
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
