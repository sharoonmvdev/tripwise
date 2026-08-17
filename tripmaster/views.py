from django.shortcuts import render,get_object_or_404

from rest_framework.views import APIView

from rest_framework.response import Response

from tripmaster.serializers import UserSerializer,TripSerializer,TripMemberSerializer

from django.contrib.auth.models import User

from tripmaster.models import Trip,TripMember

from rest_framework import authentication,permissions

from rest_framework import serializers

from tripmaster.permissions import OwnerOnly

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

    permission_classes = [OwnerOnly]

    def get(self,request,pk):

        trip_object = get_object_or_404(Trip,id=pk)

        self.check_object_permissions(request,trip_object)

        serializer_instance = TripSerializer(trip_object)

        return Response(data=serializer_instance.data)


    def put(self,request,pk):

        trip_object = get_object_or_404(Trip,id=pk)

        self.check_object_permissions(request,trip_object)

        form_data = request.data

        serializer_instance = TripSerializer(data=form_data,instance=trip_object)

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data=serializer_instance.data)

        else:

            return Response(data=serializer_instance.errors)


    def delete(self,request,pk):

        trip_object = get_object_or_404(Trip,id=pk)

        self.check_object_permissions(request,trip_object)

        trip_object.delete()

        return Response(data={"message":"deleted.."})

    

class AddMemberView(APIView):

    authentication_classes=[authentication.BasicAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def post(self,request,pk):

        trip_id = pk

        trip_object = get_object_or_404(Trip,id =trip_id)

        form_data = request.data

        serializer_instance = TripMemberSerializer(data=form_data)

        if serializer_instance.is_valid():

            serializer_instance.save(trip=trip_id)

            return Response(data=serializer_instance.data)

        else:

            return Response(data=serializer_instance.errors)

    

    














            


