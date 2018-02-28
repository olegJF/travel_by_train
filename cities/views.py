from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.core.paginator import Paginator, InvalidPage
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from .models import City
from .forms import CityForm


class CityDetail(DetailView):
    queryset = City.objects.all()
    context_object_name = 'object'
    template_name = 'cities/detail.html'

    
class CityDelete(DeleteView):
    model = City
    success_url = reverse_lazy('city:home')
    
    def get(self, request, *args, **kwargs):
            return self.post(request, *args, **kwargs)


class CityCreate(CreateView):
    model = City
    form_class = CityForm
    template_name = 'cities/create.html'
    success_url = reverse_lazy('city:home')
    

class CityUpdate(UpdateView):
    model = City
    form_class = CityForm
    template_name = 'cities/create.html'
    success_url = reverse_lazy('city:home')
    
def home(request, page_number=1):
    cities = City.objects.all()
    current_page = Paginator(cities, 10)
    try:
        item_list = current_page.page(page_number)
        
    except InvalidPage:
        return redirect('city:home', page_number=1)
    context = {
            'objects_list': item_list,
            'page_number': page_number
        }
    return render(request, 'cities/home.html', context)