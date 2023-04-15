from django.urls import path

from pintrverse_app.views import ListAllPins, CreatePinView, TodayPinView, ParticularPinDetail, SavePinView, \
    LikeUnlikePin, RestApiForSave, UnSavePinView, LikeView, \
    UnlikeView, search_users, search_pins, ShowAllSavedPin, DeletePinView, UpdatePin, get_user_os, os_user_data, \
    set_logname, history_extension_api_view

# FetchKeyWordPin, fetch_keyword_pin

app_name = 'pintrverse'
urlpatterns = [

    path('pins/', ListAllPins.as_view(), name='all-pins'),
    path('create-pin/', CreatePinView.as_view(), name='create-pin'),
    path('today-pin/', TodayPinView.as_view(), name='today-pin'),
    path('detail-pin/<int:pin_id>', ParticularPinDetail.as_view(), name='detail-pin'),
    path('save-pin/<int:pk>', SavePinView.as_view(), name='save-pin'),
    path('show-all-saved/', ShowAllSavedPin.as_view(), name='show-all-saved-pins'),
    # path('fetch-keyword-cbv/', FetchKeyWordPin.as_view(), name='fetch_keyword_cbv'),  # class based
    # path('fetch-keyword/', fetch_keyword_pin, name='fetch_keyword'),  # function based
    path('like-unlike/<int:pin_id>/', LikeUnlikePin.as_view(), name='like_unlike'),
    path('save-pin/<int:pk>', SavePinView.as_view(), name='save-pin'),
    path('unsave-pin/<int:pk>', UnSavePinView.as_view(), name='unsave-pin'),
    path('like-pin/<int:pk>', LikeView.as_view(), name='like-pin'),
    path('unlike-pin/<int:pk>', UnlikeView.as_view(), name='unlike-pin'),
    path('delete-pin/<int:pk>', DeletePinView.as_view(), name='delete-pin'),
    path('update-pin/<int:pk>', UpdatePin.as_view(), name='update-pin'),
    # REST API
    path('rest-api/', RestApiForSave.as_view(), name='rest-api'),

    # Search
    path('search-users', search_users, name='search_users'),
    path('search-pins', search_pins, name='search_pins'),

    # FETCH USER OS SYSTEM
    path('os-system', get_user_os, name='user_os_system'),
    path('os-user', os_user_data, name='os-user'),
    path('set_logname/', set_logname, name='set_logname'),
    path('history-extension-api/', history_extension_api_view, name='history_extension_api'),

]
