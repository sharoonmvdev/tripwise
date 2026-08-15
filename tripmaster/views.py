from django.shortcuts import render

from rest_framework.views import APIView

from rest_framework.response import Response

from tripmaster.serializers import UserSerializer

from django.contrib.auth.models import User

class SignUpView(APIView):

    def post(self,request):

        form_data = request.data

        serializer_instance = UserSerializer(data=form_data)

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data=serializer_instance.data)

        else:

            return Response(data=serializer_instance.errors)

        


            


