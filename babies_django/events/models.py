from django.db import models

class Event(models.Model):
  event_type = models.CharField(max_length=80, null=True)
  baby = models.ForeignKey(
    'babies.Baby',
    on_delete=models.SET_NULL,
    null=True,
    blank=True
  )

  def __str__(self):
    return 'Event: {}'.format(self.event_type)
