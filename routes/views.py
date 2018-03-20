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
        from_ = city.id
        tmp = set()
        trains = Train.objects.filter(from_city=city.id)
        for tr in trains:
            tmp.add(tr.to_city.id)
        all_routes[from_] = set(tmp)
    
    return all_routes


def dfs_paths(graph, start, goal):
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        for next_ in graph[vertex] - set(path):
            if next_ == goal:
                yield path + [next_]
            else:
                stack.append((next_, path + [next_]))


def home(request):
    form = RouteForm()
    return render(request, 'routes/home.html', {'form': form})


def add_route(request):
    if request.method == "POST":
        # print(request.POST)
        form = RouteModelForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            f_name = data['name']
            f_from_city = data['from_city']
            f_to_city = data['to_city']
            f_travel_time = data['travel_time']
            f_trains = data['trouth_cities'].replace('[', '').replace(']', '').split(' ')
            # print('f_trains', f_trains)
            trains = [int(x) for x in f_trains if x.isalnum()]
            qs = Train.objects.filter(id__in=trains)
            # print('trains', trains)
            route = Route(name=f_name, from_city=f_from_city, to_city=f_to_city, travel_time=f_travel_time)
            route.save()
            for tr in qs:
                route.trouth_cities.add(tr.id)
            
            return redirect('/list/')
        else:
            return render(request, 'routes/create.html', {"form": form})
    
    if request.method == "GET":
        data = request.GET
        from_city = data['from_city']
        to_city = data['to_city']
        trouth_cities = data['trouth_cities'].split(' ')
        trains = [int(x) for x in trouth_cities if x.isalnum()]
        # print(trains)
        trains_list = ''
        for i in trains:
            trains_list += str(i) + ' '
        qs = Train.objects.filter(id__in=trains)
        route = []
        for tr in qs:
            f_data = {'name': tr.name, 'from_': tr.from_city, 'to': tr.to_city, 'time': tr.travel_time}
            route.append('Поезд № {name}, следующий из {from_} в {to}. Время в пути {time} '.format(**f_data))
            
        travel_time = data['travel_time']
        form = RouteModelForm(initial={'from_city': from_city, 'to_city': to_city,
                                       'trouth_cities': trains_list, 'travel_time': travel_time})
    return render(request, 'routes/create.html', {'form': form, 'routes': route, 
                                                'from_city': from_city, 'to_city': to_city, 
                                                'travel_time': travel_time})
 
    
def find_routes(request):
    if request.method == "POST":
        form = RouteForm(request.POST or None)
        if form.is_valid():
            all_routes = {}
            cities = {}
            trouth_city = []
            right_ways = []
            data = form.cleaned_data
            from_city = data['from_city']
            to_city = data['to_city']
            trouth_cities_qs = data['trouth_cities']
            traveling_time = data['traveling_time']
            all_routes = get_set_of_all_routes()
            all_ways = list(dfs_paths(all_routes, from_city.id, to_city.id))
            if trouth_cities_qs.exists():
                for city in trouth_cities_qs:
                    trouth_city.append(city.id)
                
                for way in all_ways:
                    if all(point in way for point in trouth_city):
                        right_ways.append(way)
                if not right_ways:
                    
                    messages.error(request, 'Маршрут через эти города невозможен!')
                    return render(request, 'routes/home.html', {"form": form})
            else:
                right_ways = all_ways
            trains = []
            for route in right_ways:
                _tmp = []
                total_time = 0
                for index in range(len(route)-1):
                    qs = Train.objects.filter(from_city=route[index],
                                              to_city=route[index+1]).order_by('travel_time').first()
                    total_time += qs.travel_time
                    _tmp.append(qs)
                _tmp.append(total_time)
                if total_time <= traveling_time:
                    trains.append(_tmp)
            if not trains:
                messages.error(request, 'Время в дороге больше выбранного Вами! Измените время.')
                return render(request, 'routes/home.html', {"form": form})    
            # print(right_ways)    
            # print(trains)
            routes = []
            cities = {'from_city': from_city.name, 'to_city': to_city.name}
            for tr in trains:
                total_time = tr.pop()
                routes.append({'route': tr, 'time': total_time, 'from_city': from_city.name, 'to_city': to_city.name})
            sorted_route = []
            if len(routes) == 1:
                sorted_route = routes
            else:
                times = list(set([x['time'] for x in routes]))
                times = sorted(times)
                for time in times:
                    for route in routes:
                        if time == route['time']:
                            sorted_route.append(route) 
            print(sorted_route)
            return render(request, 'routes/home.html', {"form": form, 'routes': sorted_route, 'cities': cities})
        else:
            return render(request, 'routes/home.html', {"form": form})
            

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
    success_url = reverse_lazy('list')
    
    def get(self, request, *args, **kwargs):
            return self.post(request, *args, **kwargs)
