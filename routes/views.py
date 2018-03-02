from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, DeleteView
from django.core.urlresolvers import reverse_lazy

from trains.models import Train
from cities.models import City
from .forms import *


def get_set_of_all_routes():
    qs = Train.objects.values('from_city')
    un = set()
    for i in qs:
        un.add(i['from_city'])
    unq_cities = City.objects.filter(pk__in=un)
    all_routes = {}
    for city in unq_cities:
        from_= city.id
        tmp = set()
        trains = Train.objects.filter(from_city=city.id)
        for tr in trains:
            tmp.add(tr.to_city.id)
        all_routes[from_]=set(tmp)
    
    return all_routes

def dfs_paths(graph, start, goal):
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        for next in graph[vertex] - set(path):
            if next == goal:
                yield path + [next]
            else:
                stack.append((next, path + [next]))




def home(request):
    form = RouteForm()
    return render(request, 'routs/home.html', {'form':form})
    
def add_route(request):
    if request.method == "GET":
        print(request.GET)
    return redirect('/')
 
    
def find_routes(request):
    if request.method == "POST":
        form = RouteForm(request.POST or None)
        if form.is_valid():
            all_routes = {}
            trouth_city = []
            right_ways = []
            data = form.cleaned_data
            from_city = data['from_city'].id
            to_city = data['to_city'].id
            trouth_cities_qs = data['trouth_cities']
            traveling_time = data['traveling_time']
            # print('traveling_time', traveling_time, 'from_city', from_city, 'to_city', to_city, 'trouth_cities', trouth_cities_qs)
            all_routes = get_set_of_all_routes()
            all_ways = list(dfs_paths(all_routes, from_city, to_city))
            if trouth_cities_qs.exists():
                for city in trouth_cities_qs:
                    trouth_city.append(city.id)
                
                for way in all_ways:
                    if all(point in way for point in trouth_city):
                        right_ways.append(way)
                if not right_ways:
                    
                    messages.error(request, 'Маршрут через эти города невозможен!')
                    return render(request, 'routs/home.html', {"form": form})
            else:
                right_ways = all_ways
            trains = []
            for  route in right_ways:
                _tmp = []
                total_time = 0
                for index in range(len(route)-1):
                    qs = Train.objects.filter(from_city=route[index], to_city=route[index+1]).order_by('travel_time').first()
                    total_time += qs.travel_time
                    _tmp.append(qs)
                _tmp.append(total_time)
                if total_time <= traveling_time:
                    trains.append(_tmp)
            if not trains:
                messages.error(request, 'Время в дороге больше выбранного Вами! Измените время.')
                return render(request, 'routs/home.html', {"form": form})    
            # print(right_ways)    
            # print(trains)
            routes = []
            for tr in trains:
                total_time = tr.pop()
                routes.append({ 'route': tr, 'time': total_time})
                
            # print(routes)
            return render(request, 'routs/home.html', {"form": form, 'routes':routes})
        else:
            return render(request, 'routs/home.html', {"form": form})
            

class RouteDetail(DetailView):
    queryset = Route.objects.all()
    context_object_name = 'object'
    template_name = 'routes/detail.html'
    
    
class RouteList(ListView):
    queryset = Route.objects.all()
    context_object_name = 'objects_list'
    template_name = 'routes/list.html'
    

class RouteDelete(DeleteView):
    model = Route
    success_url = reverse_lazy('home')
    
    def get(self, request, *args, **kwargs):
            return self.post(request, *args, **kwargs)
