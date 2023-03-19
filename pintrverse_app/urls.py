from django.urls import path

from pintrverse_app.views import ListAllPins, CreatePinView, TodayPinView

app_name = 'pintrverse'
urlpatterns = [

    path('pins/', ListAllPins.as_view(), name='all-pins'),
    path('create-pin/', CreatePinView.as_view(), name='create-pin'),
    path('today-pin/', TodayPinView.as_view(), name='today-pin'),

]
