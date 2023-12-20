from django.db import models

# Create your models here.
class product(models.Model):
    name=models.CharField(max_length=50)
    description=models.TextField()
    price=models.IntegerField()
    def __str__(self):
        return "%s %s %s" %(self.name,self.description,self.price)    