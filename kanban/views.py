from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from kanban.models import Tasks, Contacts
from kanban.serializers import UserSerializer, TasksSerializer, ContactsSerializer

# Create your views here.
class TasksViewSet(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Tasks.objects.all()
        serializer_obj = TasksSerializer(tasks, many=True)
        return Response(serializer_obj.data, content_type="application/json", status=status.HTTP_200_OK)
        
    def post(self, request):
        task_data = self._extract_task_data(request)
        user = self._get_user(task_data["author_id"])
        if not user and task_data["title"]:
            return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
        task = self._create_task(task_data, user)
        serializer_obj = TasksSerializer(task)
        return Response(serializer_obj.data, content_type="application/json", status=status.HTTP_201_CREATED)

    def _extract_task_data(self, request):
        return {
            "title": request.data.get("title", ""),
            "description": request.data.get("description", ""),
            "status": request.data.get("status", ""),
            "color": request.data.get("color", ""),
            "priority": request.data.get("priority", ""),
            "members": request.data.get("members", ""),
            "author_id": request.data.get("author", {}).get("id", 0),
        }

    def _get_user(self, user_id):
        if user_id and user_id != 0:
            try:
                return User.objects.get(id=user_id)
            except User.DoesNotExist:
                return None
        return None

    def _create_task(self, task_data, user):
        return Tasks.objects.create(
            title=task_data["title"],
            description=task_data["description"],
            status=task_data["status"],
            color=task_data["color"],
            priority=task_data["priority"],
            members=task_data["members"],
            created_at=timezone.now(),
            author=user,
        )        
        
    def put(self, request, pk=None):
        task = get_object_or_404(Tasks, pk=pk)
        serializer_obj = TasksSerializer(task, data=request.data)
        if serializer_obj.is_valid():
            serializer_obj.save()
            return Response(serializer_obj.data, content_type="application/json", status=status.HTTP_200_OK)
        return Response(serializer_obj.errors, content_type="application/json", status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk=None):
        get_object_or_404(Tasks, pk=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UsersViewSet(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        users = User.objects.all()
        serialized_obj = UserSerializer(users, many=True)
        return Response(serialized_obj.data, content_type="application/json", status=status.HTTP_200_OK)
        
    def post(self, request):
        data = request.data
        if data["username"] == "":
            return Response({'statustext': request}, content_type="application/json", status=status.HTTP_400_BAD_REQUEST)
        if data["newpassword"] != data["confirmpassword"]:
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(data["username"], data["email"], data["newpassword"])
        user.first_name, user.last_name = data["firstname"], data["lastname"]
        user.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

class ContactsViewSet(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        contacts = Contacts.objects.all()
        serialized_obj = ContactsSerializer(contacts, many=True)
        return Response(serialized_obj.data, content_type="application/json", status=status.HTTP_200_OK)
        
    def post(self, request):
        contact_data = self._extract_contact_data(request)
        user = self._get_contact_user(contact_data["user_id"])
        if not contact_data["name"]:
            return Response({'error': 'Data incomplete', 'detail': contact_data}, status=status.HTTP_400_BAD_REQUEST)
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
        contact = self._create_contact(contact_data, user)
        serializer_obj = ContactsSerializer(contact)
        return Response(serializer_obj.data, content_type="application/json", status=status.HTTP_201_CREATED)

    def _extract_contact_data(self, request):
        return {
            "name": request.data.get("name", ""),
            "initials": request.data.get("initials", ""),
            "email": request.data.get("email", ""),
            "phone": request.data.get("phone", ""),
            "user_id": request.data.get("user", {}).get("id", 0),
        }

    def _get_contact_user(self, user_id):
        if user_id and user_id != 0:
            try:
                return User.objects.get(id=user_id)
            except User.DoesNotExist:
                return None
        return None

    def _create_contact(self, contact_data, user):
        return Contacts.objects.create(
            name = contact_data["name"],
            initials = contact_data["initials"],
            email = contact_data["email"],
            phone = contact_data["phone"],
            user = user,
        )        
        
    def put(self, request, pk=None):
        contact = get_object_or_404(Contacts, pk=pk)
        serializer_obj = ContactsSerializer(contact, data=request.data)
        if serializer_obj.is_valid():
            serializer_obj.save()
            return Response(serializer_obj.data, content_type="application/json", status=status.HTTP_200_OK)
        return Response(serializer_obj.errors, content_type="application/json", status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk=None):
        get_object_or_404(Contacts, pk=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LoginView(ObtainAuthToken):
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'userid': user.id, 'email': user.email})

class CurrentUserViewSet(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token_key = request.data.get("token")
        if not token_key:
            return Response({'error': 'Token not provided'}, content_type="application/json", status=status.HTTP_400_BAD_REQUEST)
        try:
            user = Token.objects.get(key=token_key).user
            return Response(UserSerializer(user).data, content_type="application/json", status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

class RegisterView(APIView):
    def post(self, request):
        register_data = self._extract_register_data(request)
        if register_data["username"] == "":
            return Response({'statustext': request}, content_type="application/json", status=status.HTTP_400_BAD_REQUEST)
        if register_data["userpasswordnew"] == register_data["userpasswordconfirm"]:
            user = User.objects.create_user(register_data["username"], register_data["email"], register_data["userpasswordnew"])
            user.first_name, user.last_name = register_data["first_name"], register_data["last_name"]
            user.save()
        if user:
            return Response(self._create_register_response(user), content_type="application/json", status=status.HTTP_201_CREATED)
        
    def _extract_register_data(self, request):
        return {
            "username" : request.data.get("username"),
            "userpasswordnew" : request.data.get("newpassword"),
            "userpasswordconfirm" : request.data.get("confirmpassword"),
            "first_name" : request.data.get("firstname"),
            "last_name" : request.data.get("lastname"),
            "email" : request.data.get("email"),
        }
        
    def _create_register_response(self, user):
        return {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }
