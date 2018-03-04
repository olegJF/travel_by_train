from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from cities.models import City


class Train(models.Model):
    name = models.CharField(max_length=50, verbose_name='Номер поезда', unique=True)
    from_city = models.ForeignKey(City, verbose_name='Откуда', on_delete=models.CASCADE, related_name="from_city")
    to_city = models.ForeignKey(City, verbose_name='Куда', on_delete=models.CASCADE, related_name="to_city")
    travel_time = models.IntegerField(verbose_name='Время в пути')
    
    def clean(self):
        if Train.objects.filter(from_city=self.from_city, to_city=self.to_city, travel_time=self.travel_time).exists():
            raise ValidationError('Измените время в пути.')
         
    class Meta:
        verbose_name = 'Поезд'
        verbose_name_plural = 'Поезда'
        ordering = ['name']
    
    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse('detail', kwargs={"pk": self.pk})
