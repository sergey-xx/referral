from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes




from referrals.models import RefCodes
from .serializers import RefCodesSerializer, EmailSerializer, UserRetriveSerializer

User = get_user_model()

class UserViewSet(mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):

    queryset = User.objects.all()
    serializer_class = UserRetriveSerializer
    permission_classes = (AllowAny, )
    http_method_names = ['get', 'post']


class RefCodesViewSet(APIView):
    """ViewSet для просмотра и редактирования реферрального кода."""

    permission_classes = (IsAuthenticated, )

    def get(self, request):
        code = get_object_or_404(RefCodes, user=request.user)
        serializer = RefCodesSerializer(code)
        return Response(serializer.data)

    def post(self, request, format=None):
        print(request.data)
        if RefCodes.objects.filter(user=request.user).exists():
            return Response('Вы можете создать только 1 код',
                        status=status.HTTP_400_BAD_REQUEST) 
        data = request.data
        data['user'] = request.user.id
        print(data)
        serializer = RefCodesSerializer(data=data,)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, format=None):
        code = get_object_or_404(RefCodes, user=request.user)
        code.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST', ])
@permission_classes((AllowAny, ))
def send_code(request):
    data = request.data
    serializer = EmailSerializer(data=data)
    if serializer.is_valid():
        user_email = serializer.data.get('email')
        code = RefCodes.objects.filter(user__email=user_email).first()
        if code:
            send_mail(message=code.code,
                      from_email=settings.SERVER_EMAIL,
                      recipient_list=[user_email],
                      subject='Ваш реферальный код')
            return Response('Реферальный код отправлен на вашу почту',
                            status=status.HTTP_201_CREATED,)
        return Response('У вас нет кода',
                    status=status.HTTP_400_BAD_REQUEST,)
    return Response('Почта не зарегистрирована',
                    status=status.HTTP_400_BAD_REQUEST,)
