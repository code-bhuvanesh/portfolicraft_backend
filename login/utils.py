from django.contrib.auth import authenticate
from django.contrib.auth.models import User

def userLogin(email, password):
    username = User.objects.get(email=email.lower()).username
    user = authenticate(username=username, password=password)
    return user