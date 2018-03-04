from django.db import models
from django.urls import reverse


class City(models.Model):
    name = models.CharField(max_length=50, verbose_name='Населенный пункт', unique=True)
    
    class Meta:
        verbose_name = 'Населенный пункт'
        verbose_name_plural = 'Населенные пункты'
        ordering = ['name']
    
    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse('detail', kwargs={"pk": self.pk})
