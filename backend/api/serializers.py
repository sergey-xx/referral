from rest_framework import serializers

from referrals.models import RefCodes, Invited
from django.contrib.auth import get_user_model

User = get_user_model()

class RefCodesSerializer(serializers.ModelSerializer):

    class Meta:
        model = RefCodes
        fields = ('id', 'code', 'pub_date', 'expiration', 'user',)
        read_only_fields = ('id', 'pub_date',)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id',
                  'first_name',
                  'last_name',
                  'email',
                  'username',)
        # read_only_fields = ('id', 'pub_date', 'user')


class InvitedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invited
        fields = ('id', 'code', 'pub_date', 'expiration', 'user',)
        read_only_fields = ('id', 'pub_date', 'user')