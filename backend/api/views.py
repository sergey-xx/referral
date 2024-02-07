from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView



from referrals.models import RefCodes
from .serializers import RefCodesSerializer

User = get_user_model()


# class RefCodesViewSet(mixins.UpdateModelMixin,
#                mixins.DestroyModelMixin,
#                mixins.CreateModelMixin,
#                mixins.RetrieveModelMixin,
#                viewsets.GenericViewSet):
#     """ViewSet для просмотра и редактирования реферрального кода."""
#     queryset = RefCodes.objects.all()
#     serializer_class = RefCodesSerializer
#     permission_classes = (IsAuthenticated, )
#     http_method_names = ['get', 'post', 'delete']

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

#     def create(self, request, *args, **kwargs):
#         if RefCodes.objects.filter(user=request.user).exists():
#             return Response('Вы можете создать только 1 код',
#                         status=status.HTTP_400_BAD_REQUEST)
#         return super().create(request, *args, **kwargs)
    
#     def destroy(self, request, *args, **kwargs):

#         return super().destroy(request, *args, **kwargs)


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