from django.db import models

class Baby(models.Model):
  name = models.CharField(max_length=200)
  age = models.PositiveIntegerField()
  parent = models.ForeignKey(
    'parents.Parent',
    on_delete=models.SET_NULL,
    null=True,
    blank=True
  )

  def __str__(self):
    return 'Babie: {}'.format(self.name)