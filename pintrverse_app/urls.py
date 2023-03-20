from django.urls import path

from pintrverse_app.views import ListAllPins, CreatePinView, TodayPinView, ParticularPinDetail, SavePinView, \
    ShowAllSavedPin

app_name = 'pintrverse'
urlpatterns = [

    path('pins/', ListAllPins.as_view(), name='all-pins'),
    path('create-pin/', CreatePinView.as_view(), name='create-pin'),
    path('today-pin/', TodayPinView.as_view(), name='today-pin'),
    path('detail-pin/<int:pin_id>', ParticularPinDetail.as_view(), name='detail-pin'),
    path('save-pin/<int:pk>', SavePinView.as_view(), name='save-pin'),
    path('show-all-saved/', ShowAllSavedPin.as_view(), name='show-all-saved-pins'),

]
