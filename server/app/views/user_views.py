from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User


# Create your views here.
class UserListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser, IsAuthenticated]

    def get(self, request, format=None):
        # usernames = [user.username for user in User.objects.all()]
        # return Response(usernames)
        user = User.objects.all()
        listOfCredentials = dict()
        i = 1
        for u in user:
            listOfCredentials[u.id] = {'username': u.username, 'email': u.email, 'password': u.password}
            i += 1
        print(str(listOfCredentials))
        return Response(listOfCredentials)

    def put(self, request):
        username = request.data.get('username', request.user.username)
        password = request.data.get('password', request.user.password)
        email = request.data.get('email', request.user.email)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': f"User {username} do not exist OR wrong credentials"})
        user.username = username
        user.password = password
        user.email = email
        user.save()
        return Response({'success': "The details were updated"})

    def delete(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        try:
            user = User.objects.get(username=username, password=password)
        except User.DoesNotExist:
            return Response({'error': f"User {username} do not exist OR wrong credentials"})
        Token.objects.get(user=user).delete()
        user.delete()
        return Response({'Success': f"User {username} was deleted"})


class RegisterSimpleView(APIView):
    def post(self, request, format=None):
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        if not username or not password or not email:
            return Response({'error': 'Please provide all required fields'})
        try:
            user = User.objects.create_user(username=username, password=password, email=email)
        except Exception as e:
            return Response({'error': str(e)})
        if user:
            token, created = Token.objects.get_or_create(user=user)
            print(user.username)
            return Response({'token': str(token), 'created': created})
        # User.objects.all().delete()
        # Token.objects.all().delete()
        # return Response("deleted")


class RegisterAdminView(APIView):
    def post(self, request, format=None):
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        if not username or not password or not email:
            return Response({'error': 'Please provide all required fields'})
        try:
            user = User.objects.create_superuser(username=username, password=password, email=email)
        except Exception as e:
            return Response({'error': str(e)})
        if user:
            token, created = Token.objects.get_or_create(user=user)
            print(user.username)
            return Response({'token': str(token), 'created': created})


class LoginView(APIView):
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        # email = request.POST['email']
        user = authenticate(request, username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'})


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response({'message': 'Logged out successfully'})
