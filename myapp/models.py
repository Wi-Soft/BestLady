from django.db import models

# Create your models here.

class Header(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='img/')

    def __str__(self):
        return self.name
    
class Hair(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='img/')

    def __str__(self):
        return self.name
    
class Nail(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='img/')

    def __str__(self):
        return self.name
    



    from django.db import models

