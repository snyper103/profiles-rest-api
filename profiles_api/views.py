from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.
class HelloAPIView(APIView):
	"""Test API view"""
	def get(self, request, format=None):
		"""Returns a list of APIView features"""
		an_apiview = [
			'Uses HTTP methods as fuction (get, post, patch, put, and delete)',
			'Is similar to a traditional Django View',
			'Gives you the most control over your application logic',
			'Is mapped manually to URLs',
		]

		# It converts an object to a json, in order to convert to a json it needs to be either a list or dictionary
		return Response({
			'message': 'Hello!',
			'an_apiview': an_apiview
		 })	# Returning a dictionary