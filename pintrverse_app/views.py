import datetime

from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from pintrverse_app.forms import CreatePinForm
from pintrverse_app.models import Pin, SavedPin, Tag
from pintrverse_app.utils import extract_keywords, get_history_list


# Create your views here.
class ListAllPins(generic.ListView):
    model = Pin
    template_name = 'pintrverse_app/pin_list.html'


class CreatePinView(generic.CreateView):
    model = Pin
    template_name = 'pintrverse_app/create_pin.html'
    form_class = CreatePinForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreatePinView, self).form_valid(form)


class TodayPinView(generic.ListView):
    model = Pin
    template_name = 'pintrverse_app/todays_pin.html'
    queryset = Pin.objects.filter(created_at__date=datetime.date.today())


class ParticularPinDetail(generic.DetailView):
    model = Pin
    template_name = 'pintrverse_app/particular_pin.html'
    slug_url_kwarg = 'pin_id'
    slug_field = 'id'


class SavePinView(generic.View):

    def post(self, request, *args, **kwargs):
        pin_id = kwargs['pk']
        save_p = SavedPin.objects.create(user_id=request.user.id,
                                         pin_id=pin_id)
        return redirect(to='home')


class ShowAllSavedPin(generic.ListView):
    model = SavedPin
    template_name = 'pintrverse_app/show_all_saved_pins.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        # Add custom filtering or ordering to the queryset
        queryset = queryset.filter(user_id=self.request.user.id)
        return queryset


# FUNCTIONAL BASED FETCH PIN FROM USER's history's keyword
def fetch_keyword_pin(request):
    keywords = extract_keywords(get_history_list(5))
    for keyword in keywords:
        fetched_tag = Tag.objects.filter(name=str(keyword))
        break
    fetched_pin = Pin.objects.filter(tag__id__in=fetched_tag.all())
    return HttpResponse(fetched_pin)


class FetchKeyWordPin(generic.ListView):
    model = Pin
    template_name = 'pintrverse_app/fetched_pin.html'
    keywords = extract_keywords(get_history_list(5))  # function for fetch history & filter keywords from that
    ls = []
    for keyword in keywords:
        if fetched_tag := Tag.objects.filter(name=str(keyword)):  # find TAGS Based on keyword [ history ]
            for i in fetched_tag.all():
                queryset = Pin.objects.filter(tag=i.id)  # Find Pin based on Tag
                ls.append(queryset)
        queryset = []
        for j in ls:
            queryset += j
