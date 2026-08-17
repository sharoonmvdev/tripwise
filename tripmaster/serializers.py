
from rest_framework import serializers

from django.contrib.auth.models import User

from tripmaster.models import Trip,TripMember

class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = ["username","email","password"]

    def create(self,validated_data):

        return User.objects.create_user(**validated_data)


class TripMemberSerializer(serializers.ModelSerializer):

    member = serializers.StringRelatedField()

    class Meta:

        model = TripMember

        fields = "__all__"

        read_only_fields = ["id","trip","role","joined_at"]


class TripSerializer(serializers.ModelSerializer):

    created_by =serializers.StringRelatedField(read_only=True)

    member_count = serializers.SerializerMethodField(read_only=True)

    trip_members= serializers.SerializerMethodField(read_only=True)

    class Meta:

        model = Trip

        fields = "__all__"

        read_only_fields = ["id","created_by","created_at","updated_at","members","trip_members"]

    def get_member_count(self,trip_obj):

        # obj => trip_obj

        return TripMember.objects.filter(trip=trip_obj).count()

    def get_trip_members(self,obj):

        members = TripMember.objects.filter(trip=obj)

        serializer_instance = TripMemberSerializer(members,many=True)

        return serializer_instance.data

    
 



    

    






    


