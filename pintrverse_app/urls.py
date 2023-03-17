from django.urls import path

from pintrverse_app.views import ListAllPins

app_name = 'pintrverse'
urlpatterns = [

    path('pins/', ListAllPins.as_view(), name='all-pins'),

]
