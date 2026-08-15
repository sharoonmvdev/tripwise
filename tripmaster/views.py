from django.shortcuts import render,get_object_or_404

from rest_framework.views import APIView

from rest_framework.response import Response

from tripmaster.serializers import UserSerializer,TripSerializer

from django.contrib.auth.models import User

from tripmaster.models import Trip

from rest_framework import authentication,permissions

from rest_framework import serializers

class SignUpView(APIView):

    def post(self,request):

        form_data = request.data

        serializer_instance = UserSerializer(data=form_data)

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data=serializer_instance.data)

        else:

            return Response(data=serializer_instance.errors)


class TripListCreateView(APIView):

    authentication_classes = [authentication.BasicAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):

        qs = Trip.objects.filter(created_by=request.user)

        sereializer_instance = TripSerializer(qs,many=True)

        return Response(data=sereializer_instance.data)

    def post(self,request):

        form_data = request.data

        serializer_instance = TripSerializer(data=form_data)

        if serializer_instance.is_valid():

            serializer_instance.save(created_by = request.user)

            #cleaned_data = serializer_instance.validated_data

            #Trip.objects.create(**cleaned_data,created_by = request.user)

            return Response(data=serializer_instance.data)

        else:

            return Response(data=serializer_instance.errors)


class TripRetrieveUpdateDeleteView(APIView):

    authentication_classes = [authentication.BasicAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def get(self,request,pk):

        trip_object = get_object_or_404(Trip,id=pk)

        if trip_object.created_by == request.user:

            serializer_instance = TripSerializer(trip_object)

            return Response(data=serializer_instance.data)

        else:

            raise serializers.ValidationError("you donot have the permission to perfrm this action")



    def put(self,request,pk):

        trip_object = get_object_or_404(Trip,id=pk)

        if trip_object.created_by != request.user:

            raise serializers.ValidationError("access denied..")

        form_data = request.data

        serializer_instance = TripSerializer(data=form_data,instance=trip_object)

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data=serializer_instance.data)

        else:

            return Response(data=serializer_instance.errors)


    def delete(self,request,pk):

        trip_object = get_object_or_404(Trip,id=pk)

        if trip_object.created_by != request.user:

            raise serializers.ValidationError("access denied...")

        trip_object.delete()

        return Response(data={"message":"deleted.."})

    

       














            


