from django.db import models


class Keys(models.Model):
    id = models.BigAutoField(primary_key=True)
    key = models.TextField(max_length=150)

    class Meta:
        db_table = 'keys'
        unique_together = (('key', 'id'),)


class Requests(models.Model):
    id = models.BigAutoField(primary_key=True)
    ip = models.TextField(max_length=46)
    auth_key = models.TextField(max_length=150)
    user_agent = models.TextField(max_length=200)
