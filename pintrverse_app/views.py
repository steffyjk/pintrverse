import datetime

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from pintrverse_app.forms import CreatePinForm
from pintrverse_app.models import Pin, SavedPin


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
