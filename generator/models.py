from django.db import models
from django.template.defaulttags import register

# Create your models here.
class Galaxy_Cluster(models.Model):
    redshift = models.FloatField()
    lambda_l = models.FloatField()
    lambda_m = models.FloatField()
    hubble_c = models.FloatField()

    def __str__(self):
        string = ''
        for value, key in vars(self).values():
            string += f'{key}: {value}\n'
        return string[:-1]


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)