from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated, SAFE_METHODS
from api.serializers import *
from django.core.exceptions import PermissionDenied

class CountryView(ModelViewSet):
    permission_classes=IsAuthenticated
    serializer_class=CountrySerializer
    queryset= Country.objects.all()

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
class 

