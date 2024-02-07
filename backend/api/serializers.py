from rest_framework import serializers

from referrals.models import RefCodes, Invited
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()

class RefCodesSerializer(serializers.ModelSerializer):

    class Meta:
        model = RefCodes
        fields = ('id', 'code', 'pub_date', 'expiration', 'user',)
        read_only_fields = ('id', 'pub_date',)


class UserCreateSerializer(serializers.ModelSerializer):
    code = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id',
                  'email',
                  'username',
                  'code')
    
    def validate_code(self, code):
        if not RefCodes.objects.filter(code=code).exists():
            raise serializers.ValidationError('Код не найден!')
        exp_date = RefCodes.objects.get(code=code).expiration
        if exp_date < date.today():
            raise serializers.ValidationError('Код просрочен!')
        return code
    
    def create(self, validated_data):
        code = validated_data.pop('code')
        instance = super(UserCreateSerializer, self).create(validated_data)
        referrer = User.objects.filter(code__code=code).first()
        invitee = User.objects.get(id=instance.id)
        Invited.objects.create(referrer=referrer, invitee=instance)
        return instance


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id',
                  'first_name',
                  'last_name',
                  'email',
                  'username',)


class UserRetriveSerializer(serializers.ModelSerializer):
    referrals = UserSerializer()
    class Meta:
        model = User
        fields = ('id',
                  'first_name',
                  'last_name',
                  'email',
                  'username',
                  'referrals')


class InvitedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invited
        fields = ('id', 'code', 'pub_date', 'expiration', 'user',)
        read_only_fields = ('id', 'pub_date', 'user')


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ('email',)

    def validate_email(self, email):
        print('>>>>>>>>>>>>>>')
        print(email)
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Почта не зарегистрирована!')
        return email