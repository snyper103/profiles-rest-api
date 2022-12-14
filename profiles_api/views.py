from rest_framework import status, viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated	# If you want to none authenticated profiles read only, uses IsAuthenticatedOrReadOnly insted of IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken

from profiles_api import models, serializers, permissions


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


class HelloViewSet(viewsets.ViewSet):
	"""Test API ViewSet"""
	serializer_class = serializers.HelloSerializer

	def list(self, request, format=None):
		"""Return a hello message"""
		aViewSet = [
			'Uses actions (list, create, retrieve, update, partial_update)',
			'Automatically maps to URLs using Routers',
			'Provides more functionality with less code',
		]

		return Response({
			'msg': 'Hello!',
			'aViewSet': aViewSet
			})

	def create(self, request):
		"""Create a new hello message"""
		serializer = self.serializer_class(data=request.data)

		if serializer.is_valid():
			firstName = serializer.validated_data.get('first_name')
			message = {'msg': f'Hello {firstName}'}
			statusMsg = status.HTTP_200_OK
		else :
			message = serializer.errors
			statusMsg = status.HTTP_400_BAD_REQUEST

		return Response(message, status=statusMsg)

	def retrieve(self, request, pk=None):
		"""Handle getting an object by its ID"""
		return Response({'http_method': 'GET'})

	def update(self, request, pk=None):
		"""Handle updating an object"""
		return Response({'http_method': 'PUT'})

	def partial_update(self, request, pk=None):
		"""Handle updating part of an object"""
		return Response({'http_method': 'PATCH'})

	def destroy(self, request, pk=None):
		"""Handle deleting an object"""
		return Response({'http_method': 'DELETE'})


class UserProfileViewSet(viewsets.ModelViewSet):
	"""Handle creating and updating profiles"""
	serializer_class = serializers.UserProfileSerializer
	
	queryset = models.UserProfile.objects.all()
	filter_backends = (filters.SearchFilter,)
	search_fields = ('name', 'email',)
	
	authentication_classes = (TokenAuthentication,)
	permission_classes = (permissions.UpdateOwnProfile,)


class UserLoginAPIView(ObtainAuthToken):
	"""Handle creating user authentication tokens"""
	renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFeedViewSet(viewsets.ModelViewSet):
	"""Handles creating, reading and updating profile feed items"""
	serializer_class = serializers.ProfileFeedItemSerializer

	authentication_classes = (TokenAuthentication,)
	permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

	queryset = models.ProfileFeedItem.objects.all()

	def perform_create(self, serializer):
		"""Sets the user profile to the logged in user"""
		serializer.save(user_profile=self.request.user)