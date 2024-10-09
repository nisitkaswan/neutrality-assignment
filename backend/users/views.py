# backend/users/views.py
import random
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer

class RandomUserList(APIView):
    def get(self, request):
        users = list(User.objects.all())
        if not users:
            return Response({"error": "No users found"}, status=404)

        random_users = random.sample(users, min(5, len(users)))

        serializer = UserSerializer(random_users, many=True)
        return Response(serializer.data)