import datetime

from django.urls import reverse_lazy
from django.views import generic

from pintrverse_app.forms import CreatePinForm
from pintrverse_app.models import Pin


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
