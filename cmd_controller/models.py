from django.db import models


class CommandController(models.Model):
    script_name = models.CharField(max_length=256, unique=True)
    is_reentrant = models.BooleanField(default=False)
    # is_run = models.BooleanField(default=False)
    #is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    # ToDO: add user fk for following fields
    # created_by = models.ForeignKey
    # updated_by =


