from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.core.paginator import Paginator, InvalidPage
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from .models import Train
from .forms import TrainForm


class TrainDetail(DetailView):
    queryset = Train.objects.all()
    context_object_name = 'object'
    template_name = 'trains/detail.html'

    
class TrainDelete(DeleteView):
    model = Train
    success_url = reverse_lazy('train:home')
    
    def get(self, request, *args, **kwargs):
            return self.post(request, *args, **kwargs)


class TrainCreate(CreateView):
    model = Train
    form_class = TrainForm
    template_name = 'trains/create.html'
    success_url = reverse_lazy('train:home')
    

class TrainUpdate(UpdateView):
    model = Train
    form_class = TrainForm
    template_name = 'trains/create.html'
    success_url = reverse_lazy('train:home')


def home(request, page_number=1):
    trains = Train.objects.all()
    current_page = Paginator(trains, 10)
    try:
        item_list = current_page.page(page_number)
        
    except InvalidPage:
        return redirect('train:home', page_number=1)
    context = {
            'objects_list': item_list,
            'page_number': page_number
        }
    return render(request, 'trains/home.html', context)
