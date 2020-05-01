from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from permissions.services import APIPermissionClassFactory

from babies.models import Baby
from events.models import Event
from parents.models import Parent

from babies.serializers import BabySerializer
from events.serializers import EventSerializer
from parents.serializers import ParentSerializer


def evaluate_permission(user, obj, request):
    return user.name == obj.parent.name

class BabyViewSet(viewsets.ModelViewSet):
  queryset = Baby.objects.all()
  serializer_class = BabySerializer
  permission_classes = (
    APIPermissionClassFactory(
      name='BabyPermission',
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
          'events': evaluate_permission,
        }
      }
    ),
  )

  def perform_create(self, serializer):
    baby = serializer.save()
    user = self.request.user
    assign_perm('babys.change_baby', user, baby)
    return Response(serializer.data)

  @action(detail=True, url_path='events', methods=['get'])
  def events(self, request, pk=None):
    baby = self.get_Object()
    event_list = Event.objects.filter(baby = baby)
    response = EventSerializer(event_list, many = True).data
    return Response(response)


