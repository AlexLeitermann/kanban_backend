from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from kanban.models import Tasks, Contacts
from kanban.serializers import UserSerializer, TasksSerializer, ContactsSerializer



# Create your views here.
class TasksViewSet(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] #[permissions.IsAdminUser]

    serializer_class = TasksSerializer

    def get(self, request, format=None):
        tasks = Tasks.objects.all()
        serializer_obj = TasksSerializer(tasks, many=True)
        return Response(serializer_obj.data, status=status.HTTP_200_OK, content_type="application/json")
        # return Response({'status': 'OK - GET Tasks'})
        
    def post(self, request):
        title = request.data['title']
        description = request.data['description']
        task_status = request.data['status']
        color = request.data['color']
        priority = request.data['priority']
        members = request.data['members']
        author_data = request.data.get('author', None)
        user_id = author_data.get('id') if isinstance(author_data, dict) else author_data
        if title != '':
            user = None
            if user_id != 0:
                try:
                    user = User.objects.get(id=user_id)
                    # user = Token.objects.get(key='token string').user
                except User.DoesNotExist:
                    return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
            task = Tasks.objects.create(
                title = title, 
                description = description, 
                status = task_status, 
                color = color,
                priority = priority,
                members = members,
                created_at = timezone.now(),
                author = user
            )
            task.save()
            serializer_obj_user = UserSerializer(user)
            return Response({
                        'title': task.title,
                        'description': task.description,
                        'status': task.status,
                        'color': task.color,
                        'priority': task.priority,
                        'members': task.members,
                        'created_at': task.created_at,
                        'author': serializer_obj_user.data
                        }, 
                            content_type="application/json", 
                            status=status.HTTP_201_CREATED)
        return Response({'statustext': request, 'anfrage': request.data}, content_type="application/json", status=status.HTTP_400_BAD_REQUEST)
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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] #[permissions.IsAdminUser]

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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] #[permissions.IsAdminUser]

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
            'userid': user.id,
            'email': user.email
        })

class CurrentUserViewSet(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] #[permissions.IsAdminUser]

    def post(self, request):
        token_key = request.data.get("token")
        if token_key:
            try:
                user = Token.objects.get(key=token_key).user
                return Response({
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                }, content_type="application/json", status=status.HTTP_200_OK)
            except Token.DoesNotExist:
                return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'error': 'Token not provided'}, content_type="application/json", status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    def post(self, request):
        # return Response({'statustext': request}, content_type="application/json", status=status.HTTP_200_OK)
        username = request.data.get("username")
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
