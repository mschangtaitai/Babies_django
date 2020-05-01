from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from permissions.services import APIPermissionClassFactory
from django.core.exceptions import PermissionDenied

from babies.models import Baby
from events.models import Event
from parents.models import Parent

from babies.serializers import BabySerializer
from events.serializers import EventSerializer
from parents.serializers import ParentSerializer

def evaluate_permission(user, obj, request):
    return user.first_name == obj.owner.name

class ParentViewSet(viewsets.ModelViewSet):
  queryset = Parent.objects.all()
  serializer_class = ParentSerializer

  @action(detail=True, url_path='babies', methods=['get'])
  def viewBabies(self, request, pk=None):
    parent = self.get_object()
    if(parent.name == self.request.user.name):
      baby_list = Baby.objects.filter(parent = parent)
      response = BabySerializer(baby_list, many = True).data
      return Response(response)
    else:
      raise PermissionDenied()