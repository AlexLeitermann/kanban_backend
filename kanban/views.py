from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from kanban.models import Tasks, Contacts
from kanban.serializers import UserSerializer, TasksSerializer, ContactsSerializer



# Create your views here.
class TasksViewSet(APIView):
    serializer_class = TasksSerializer

    def get(self, request, format=None):
        tasks = Tasks.objects.all()
        serializer_obj = TasksSerializer(tasks, many=True)
        return Response(serializer_obj.data, status=status.HTTP_200_OK, content_type="application/json")
        # return Response({'status': 'OK - GET Tasks'})
        
    def post(self, request):
        serializer_obj = TasksSerializer(data=request.data)
        if serializer_obj.is_valid():
            serializer_obj.save()
            return Response(serializer_obj.data, status=status.HTTP_201_CREATED)
        return Response({'statustext': request}, content_type="application/json", status=status.HTTP_400_BAD_REQUEST)
        # return  Response({'status': 'OK - POST Tasks'})
        
    def put(self, request, pk=None):
        task = get_object_or_404(Tasks, pk=pk)
        serializer_obj = TasksSerializer(task, data=request.data)
        if serializer_obj.is_valid():
            serializer_obj.save()
            return Response(serializer_obj.data, status=status.HTTP_200_OK, content_type="application/json")
        return Response(serializer_obj.errors, content_type="application/json", status=status.HTTP_400_BAD_REQUEST)
        # return Response({'statustext': pk, 'text2':''}, content_type="application/json", status=status.HTTP_400_BAD_REQUEST)
        # return  Response({'status': 'OK - PUT Tasks'})
        
    def delete(self, request, pk=None):
        task = get_object_or_404(Tasks, pk=pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        # return  Response({'status': 'OK - DELETE Tasks'})

class UsersViewSet(APIView):
    def get(self, request):
        users = User.objects.all()
        serialized_obj = UserSerializer(users, many=True)
        return Response(serialized_obj.data, content_type="application/json")
        # return  Response({'status': 'OK - GET Users'})
        
    def post(self, request):
        username = request.data.get("username", "")
        userpasswordnew = request.data.get("newpassword")
        userpasswordconfirm = request.data.get("confirmpassword")
        first_name = request.data.get("firstname")
        last_name = request.data.get("lastname")
        email = request.data.get("email")
        if username != "":
            if userpasswordnew == userpasswordconfirm:
                user = User.objects.create_user(username, email, userpasswordnew)
                user.first_name = first_name
                user.last_name = last_name
                user.save()
            if user:
                return Response({
                    'user_id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    }, content_type="application/json", status=status.HTTP_201_CREATED)
        return Response({'statustext': request}, content_type="application/json", status=status.HTTP_400_BAD_REQUEST)

class ContactsViewSet(APIView):
    def get(self, request):
        contacts = Contacts.objects.all()
        serialized_obj = ContactsSerializer(contacts, many=True)
        return Response(serialized_obj.data, status=status.HTTP_200_OK, content_type="application/json")
        
    def post(self, request):
        name = request.data.get("name", "")
        initials = request.data.get("initials")
        email = request.data.get("email")
        phone = request.data.get("phone")
        user_id = request.data.get("user")
        if name != "":
            user = None
            if user_id:
                try:
                    user = User.objects.get(id=user_id)
                except User.DoesNotExist:
                    return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
            contact = Contacts.objects.create(
                name=name, 
                initials=initials, 
                email=email, 
                phone=phone,
                user=user
            )
            contact.save()
            return Response({
                        'id': contact.id,
                        'name': contact.name,
                        'initials': contact.initials,
                        'email': contact.email,
                        'phone': contact.phone,
                        # 'user': contact.user,
                        }, 
                            content_type="application/json", 
                            status=status.HTTP_201_CREATED)
        return Response({'statustext': request}, content_type="application/json", status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk=None):
        task = get_object_or_404(Contacts, pk=pk)
        serializer_obj = ContactsSerializer(task, data=request.data)
        if serializer_obj.is_valid():
            serializer_obj.save()
            return Response(serializer_obj.data, status=status.HTTP_200_OK, content_type="application/json")
        return Response(serializer_obj.errors, content_type="application/json", status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk=None):
        task = get_object_or_404(Contacts, pk=pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'email': user.email
        })

class RegisterView(APIView):
    def post(self, request):
        # return Response({'statustext': request}, content_type="application/json", status=status.HTTP_200_OK)
        username = request.data.get("email")
        userpasswordnew = request.data.get("newpassword")
        userpasswordconfirm = request.data.get("confirmpassword")
        first_name = request.data.get("firstname")
        last_name = request.data.get("lastname")
        email = request.data.get("email")
        if username != "":
            if userpasswordnew == userpasswordconfirm:
                user = User.objects.create_user(username, email, userpasswordnew)
                user.first_name = first_name
                user.last_name = last_name
                user.save()
            if user:
                return Response({
                    'user_id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    }, content_type="application/json", status=status.HTTP_201_CREATED)
        return Response({'statustext': request}, content_type="application/json", status=status.HTTP_400_BAD_REQUEST)
