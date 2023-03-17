from django.views import generic

from pintrverse_app.models import Pin


# Create your views here.
class ListAllPins(generic.ListView):
    model = Pin
    template_name = 'pintrverse_app/pin_list.html'

