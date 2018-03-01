from django.shortcuts import render
from trains.models import Train
from cities.models import City


def get_set_of_all_routes():
    qs = Train.objects.values('from_city')
    un = set()
    for i in qs:
        un.add(i['from_city'])
    unq_cities = City.objects.filter(pk__in=un)
    all_routes = {}
    for city in unq_cities:
        from_= city.name
        tmp = set()
        trains = Train.objects.filter(from_city=city.id)
        for tr in trains:
            tmp.add(tr.to_city.name)
        all_routes[from_]=set(tmp)
    
    return all_routes

def home(request):
    all_routes = get_set_of_all_routes
    print(all_routes)
    
    return render(request, 'routs/home.html', {'unq_cities':all_routes})
