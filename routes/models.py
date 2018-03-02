from django.db import models
from django.urls import reverse
from trains.models import Train


class Route(models.Model):
    name = models.CharField(max_length=50, verbose_name = 'Название маршрута', unique=True)
    from_Train = models.ForeignKey(Train, verbose_name='Откуда', on_delete=models.CASCADE, related_name="begin")
    to_Train = models.ForeignKey(Train, verbose_name='Куда', on_delete=models.CASCADE, related_name="end")
    trouth_cities = models.ManyToManyField(Train, verbose_name='Через города', blank=True, related_name="trouth_cities")
    travel_time = models.IntegerField(verbose_name='Время в пути')
    
    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'
        ordering = ['name']
    
    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse('detail', kwargs={"pk": self.pk})