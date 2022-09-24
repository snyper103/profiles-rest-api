from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from profiles_api import serializers


# Create your views here.
class HelloAPIView(APIView):
	"""Test API view"""
	serializer_class = serializers.HelloSerializer

	def get(self, request, format=None):
		"""Returns a list of APIView features"""
		anAPIView = [
			'Uses HTTP methods as fuction (get, post, patch, put, and delete)',
			'Is similar to a traditional Django View',
			'Gives you the most control over your application logic',
			'Is mapped manually to URLs',
		]

		# It converts an object to a json, in order to convert to a json it needs to be either a list or dictionary
		return Response({
			'msg': 'Hello!',
			'anAPIView': anAPIView
		 })	# Returning a dictionary

	def post(self, request):
		"""Create a hello message with our first name"""
		serializer = self.serializer_class(data=request.data)

		if serializer.is_valid():
			firstName = serializer.validated_data.get('first_name')
			message = {'msg': f'Hello {firstName}'}
			statusMsg = status.HTTP_200_OK
		else :
			message = serializer.errors
			statusMsg = status.HTTP_400_BAD_REQUEST

		return Response(message, status=statusMsg)

	def put(self, request, pk=None):
		"""Handle updating an object"""
		return Response({'method': 'PUT'})

	def patch(self, request, pk=None):
		"""Handle a partial update of an object"""
		return Response({'method': 'PATCH'})

	def delete(self, request, pk=None):
		"""Delete an object"""
		return Response({'method': 'DELETE'})