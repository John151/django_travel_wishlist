from django.db import models

# Create your models here.

# used to create table for user input, place name and whether visited already

class Place(models.Model):
    name = models.CharField(max_length=200)
    visited = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} visited? {self.visited}'