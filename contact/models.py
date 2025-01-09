from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class Owner(models.Model):
    name=models.CharField(max_length=50)


class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=50)

        #Função importante para fazer nos Models, para nomear e ficar
    def __str__(self): 
        return self.name

class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=60, blank=True)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True)
    show = models.BooleanField(default=True)
    picture = models.ImageField(blank=True, upload_to='pictures/%Y/%m/')
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        blank=True, null=True
    )
    owner = models.ForeignKey(#Peguei os usuarios que o própriop Django cria, pelo "from django.contrib.auth.models import User"
        User, 
        on_delete=models.SET_NULL, 
        blank=True, null=True
    )



    #Função importante para fazer nos Models, para nomear e ficar
    def __str__(self): 
        return f'{self.first_name} {self.last_name}'