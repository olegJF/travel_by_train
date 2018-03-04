from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from routes import views as route_views
from cities import views as city_views

from cities.models import City
from trains.models import Train
from .forms import RouteForm


class RoutesTestCase(TestCase):
    
    def setUp(self):
        self.ct_A = City.objects.create(name="A")
        self.ct_B = City.objects.create(name="B")
        self.ct_C = City.objects.create(name="C")
        self.ct_D = City.objects.create(name="D")
        self.ct_E = City.objects.create(name="E")
        t1 = Train(name='t1', from_city=self.ct_A, to_city=self.ct_B, travel_time=9)
        t1.save()
        t2 = Train(name='t2', from_city=self.ct_B, to_city=self.ct_D, travel_time=8)
        t2.save()
        t3 = Train(name='t3', from_city=self.ct_A, to_city=self.ct_C, travel_time=7)
        t3.save()
        t4 = Train(name='t4', from_city=self.ct_C, to_city=self.ct_B, travel_time=6)
        t4.save()
        t5 = Train(name='t5', from_city=self.ct_B, to_city=self.ct_E, travel_time=3)
        t5.save()
        t6 = Train(name='t6', from_city=self.ct_B, to_city=self.ct_A, travel_time=11)
        t6.save()
        t7 = Train(name='t7', from_city=self.ct_A, to_city=self.ct_C, travel_time=10)
        t7.save()
        t8 = Train(name='t8', from_city=self.ct_E, to_city=self.ct_D, travel_time=5)
        t8.save()
        t9 = Train(name='t9', from_city=self.ct_D, to_city=self.ct_E, travel_time=4)
        t9.save()

    def test_model_City_duplicate(self):
        try:
            a_city = City(name="A")
            a_city.full_clean()
        except ValidationError as e:
            self.assertEqual({'name': ['Населенный пункт with this Населенный пункт already exists.']}, e.message_dict)

    def test_model_Train_duplicate(self):
        try:
            train = Train(name='t2', from_city=self.ct_B, to_city=self.ct_D, travel_time=8)
            train.full_clean()
        except ValidationError as e:
            self.assertEqual({'name': ['Поезд with this Номер поезда already exists.'],
                              '__all__': ['Измените время в пути.']}, e.message_dict)

    def test_function_routes_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(200, response.status_code)
        self.assertEqual(route_views.home, response.resolver_match.func)
        self.assertTemplateUsed(response, template_name='routes/home.html')

    def test_CBV_detail_city_view(self):
        response = self.client.get(reverse("city:detail", kwargs={'pk': self.ct_A.id}))
        self.assertEqual(200, response.status_code)
        self.assertEqual(city_views.CityDetail.as_view().__name__, response.resolver_match.func.__name__)
        self.assertTemplateUsed(response, template_name='cities/detail.html')
        
    def test_find_all_routes_from_A_to_E(self):
        all_routes = route_views.get_set_of_all_routes()
        all_ways = list(route_views.dfs_paths(all_routes, self.ct_A.id, self.ct_E.id))
        self.assertEqual(len(all_ways), 4)

    def test_valid_form(self):
        form_data = {'from_city': self.ct_A.id, 'to_city': self.ct_E.id,
                     'trouth_cities': [self.ct_D.id], 'traveling_time': 25}
        form = RouteForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_messages_error_more_time(self):
        response = self.client.post("/find/", {'from_city': self.ct_A.id, 'to_city': self.ct_E.id,
                                               'trouth_cities': [self.ct_D.id], 'traveling_time': 5})
        self.assertContains(response, "Время в дороге больше выбранного Вами! Измените время.", 1, 200)

    def test_messages_error_another_city(self):
        response = self.client.post("/find/", {'from_city': self.ct_B.id, 'to_city': self.ct_D.id,
                                               'trouth_cities': [self.ct_C.id], 'traveling_time': 95})
        self.assertContains(response, "Маршрут через эти города невозможен!", 1, 200)    
 

