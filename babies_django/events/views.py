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
  return obj.baby.parent.username == user.username

class EventViewSet(viewsets.ModelViewSet):
  queryset = Event.objects.all()
  serializer_class = EventSerializer
  permission_classes = (
    APIPermissionClassFactory(
      name='EventPermission',
      permission_configuration={
        'base': {
          'create': True,
          'list': True,
        },
        'instance': {
          'retrieve': evaluate_permission,
          'destroy': evaluate_permission,
          'update': evaluate_permission,
          'partial_update': evaluate_permission,
          'perform_create': evaluate_permission,
        }
      }
    ),
  )

  def perform_create(self, serializer):
    user = self.request.user
    baby = Baby.objects.get(pk=self.request.data['baby'])
    print(baby.parent.username)
    print(user.username)
    
    if(baby.parent.username == user.username):
      event = serializer.save()
      assign_perm('events.view_event', user, event)
      assign_perm('events.change_event', user, event)
      return Response(serializer.data)
    else:
      raise PermissionDenied()