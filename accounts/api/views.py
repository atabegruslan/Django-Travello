from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from accounts.api.serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token

@api_view(['POST'])
def registration_view(request):
	serializer = RegistrationSerializer(data=request.data)
	data = {}
	if serializer.is_valid():
		account = serializer.save()
		data['response'] = "Successfully registered a new user"
		data['email'] = account.email
		data['username'] = account.username
		token = Token.objects.get(user_id=account.id).key
		data['token'] = token
	else:
		data = serializer.errors
		
	return Response(data)
