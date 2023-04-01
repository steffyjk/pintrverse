from django.urls import path

from pintrverse_app.views import ListAllPins, CreatePinView, TodayPinView, ParticularPinDetail, SavePinView, \
    ShowAllSavedPin, fetch_keyword_pin, FetchKeyWordPin, LikeUnlikePin, RestApiForSave, UnSavePinView, LikeView, \
    UnlikeView

app_name = 'pintrverse'
urlpatterns = [

    path('pins/', ListAllPins.as_view(), name='all-pins'),
    path('create-pin/', CreatePinView.as_view(), name='create-pin'),
    path('today-pin/', TodayPinView.as_view(), name='today-pin'),
    path('detail-pin/<int:pin_id>', ParticularPinDetail.as_view(), name='detail-pin'),
    path('save-pin/<int:pk>', SavePinView.as_view(), name='save-pin'),
    path('show-all-saved/', ShowAllSavedPin.as_view(), name='show-all-saved-pins'),
    path('fetch-keyword-cbv/', FetchKeyWordPin.as_view(), name='fetch_keyword_cbv'),  # class based
    path('fetch-keyword/', fetch_keyword_pin, name='fetch_keyword'),  # function based
    path('like-unlike/<int:pin_id>/', LikeUnlikePin.as_view(), name='like_unlike'),
    path('save-pin/<int:pk>', SavePinView.as_view(), name='save-pin'),
    path('unsave-pin/<int:pk>', UnSavePinView.as_view(), name='unsave-pin'),
    path('like-pin/<int:pk>', LikeView.as_view(), name='like-pin'),
    path('unlike-pin/<int:pk>', UnlikeView.as_view(), name='unlike-pin'),
    # REST API
    path('rest-api/', RestApiForSave.as_view(), name='rest-api')

]
