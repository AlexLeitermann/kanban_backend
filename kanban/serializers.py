from django.contrib.auth.models import User
from rest_framework import serializers
from kanban.models import Tasks, Contacts

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email' ]


class TasksSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Tasks
        fields = '__all__'


class ContactsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Contacts
        fields = '__all__'


