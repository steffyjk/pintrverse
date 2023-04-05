import datetime

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib import messages
from rest_framework.response import Response

from pintrverse_app.filters import UserFilterSet, PinFilterSet
from pintrverse_app.forms import CreatePinForm
from pintrverse_app.models import Pin, SavedPin, Tag, Like,Category
# from pintrverse_app.utils import extract_keywords, get_history_list
from users.models import User


# Create your views here.
class ListAllPins(generic.ListView):
    model = Pin
    template_name = 'pintrverse_app/pin_list.html'

    def get_context_data(self, **kwargs):
        context = super(ListAllPins, self).get_context_data(**kwargs)
        for j in context:
            print(j)
        pins = Pin.objects.all()
        if self.request.user.is_authenticated:
            pins_saved = []
            pins_liked = []
            for pin in pins:
                try:
                    saved = SavedPin.objects.get(user=self.request.user, pin=pin)
                    pins_saved.append(saved.pin.id)
                except SavedPin.DoesNotExist:
                    pass
                try:
                    liked = Like.objects.get(user=self.request.user, pin=pin)
                    pins_liked.append(liked.pin.id)
                except Like.DoesNotExist:
                    pass
            context['saved_pins'] = pins_saved
            context['liked_pins'] = pins_liked
        # login_user = self.request.user
        # # for pin in self.object_list:
        # #     save_pin = SavedPin.objects.filter(user=login_user,
        # #                                        pin=pin.id)
        # #     # if save_pin:
        # #     #     context["is_saved"] = True
        # #     # else:
        # #     context[","] = False
        # # print(f"----This is context: {context}")
        return context


class CreatePinView(generic.CreateView):
    model = Pin
    template_name = 'pintrverse_app/create_pin.html'
    form_class = CreatePinForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Your new pin created.')
        return super(CreatePinView, self).form_valid(form)
    
    def post(self,request, *args, **kwargs):
        if 'categorybtn' in request.POST:
            category = request.POST.get('category_name')
            try:
                category = Category.objects.create(name=category)
                messages.success(request,"Category Created !")
            except:
                messages.error(request,"Something Went Wrong Creating Category !")
        return super().post(request, *args, **kwargs)

class TodayPinView(generic.ListView):
    model = Pin
    template_name = 'pintrverse_app/todays_pin.html'
    queryset = Pin.objects.filter(created_at__date=datetime.date.today())

    def get_context_data(self, **kwargs):
        context = super(TodayPinView, self).get_context_data(**kwargs)
        for j in context:
            print(j)
        pins = Pin.objects.all()
        if self.request.user.is_authenticated:
            pins_saved = []
            pins_liked = []
            for pin in pins:
                try:
                    saved = SavedPin.objects.get(user=self.request.user, pin=pin)
                    pins_saved.append(saved.pin.id)
                except SavedPin.DoesNotExist:
                    pass
                try:
                    liked = Like.objects.get(user=self.request.user, pin=pin)
                    pins_liked.append(liked.pin.id)
                except Like.DoesNotExist:
                    pass
            context['saved_pins'] = pins_saved
            context['liked_pins'] = pins_liked
        return context


class ParticularPinDetail(generic.DetailView):
    model = Pin
    template_name = 'pintrverse_app/particular_pin.html'
    slug_url_kwarg = 'pin_id'
    slug_field = 'id'


class SavePinView(generic.View):

    def post(self, request, *args, **kwargs):
        if SavedPin.objects.filter(pin__id=kwargs['pk'], user=self.request.user).exists():
            messages.warning(self.request, 'Already saved')
            return redirect(to='home')
        else:
            pin_id = kwargs['pk']
            try:
                save_p = SavedPin.objects.create(user_id=request.user.id,
                                                 pin_id=pin_id)
                messages.success(self.request, 'Saved successfully')
            except Exception as e:
                messages.error(self.request, f"{e}")
                return redirect(to='home')
            return redirect(to='home')


class UnSavePinView(generic.View):

    def post(self, request, *args, **kwargs):
        try:
            saved_pin = SavedPin.objects.get(pin__id=kwargs['pk'], user=self.request.user)
            saved_pin.delete()
            messages.success(self.request, 'Unsaved Pin')
        except SavedPin.DoesNotExist:
            messages.error(self.request, "Pin Not Saved Please Save It First !")
        return redirect(to='home')


class LikeView(generic.View):

    def post(self, request, *args, **kwargs):
        if Like.objects.filter(pin__id=kwargs['pk'], user=self.request.user).exists():
            messages.warning(self.request, 'Already Liked')
            return redirect(to='home')
        else:
            pin_id = kwargs['pk']
            try:
                save_p = Like.objects.create(user_id=request.user.id,
                                             pin_id=pin_id)
                messages.success(self.request, 'Liked successfully')
            except Exception as e:
                messages.error(self.request, f"{e}")
                return redirect(to='home')
            return redirect(to='home')


class UnlikeView(generic.View):

    def post(self, request, *args, **kwargs):
        try:
            saved_pin = Like.objects.get(pin__id=kwargs['pk'], user=self.request.user)
            saved_pin.delete()
            messages.success(self.request, 'Unliked Pin')
        except Like.DoesNotExist:
            messages.error(self.request, "Pin Not Liked Please Save It First !")
        return redirect(to='home')


from rest_framework.generics import GenericAPIView


class RestApiForSave(GenericAPIView):

    def get(self, request, *args, **kwargs):
        req = self.request
        post_id = req.GET.get('post_id')
        user_id = req.GET.get('user_id')
        if SavedPin.objects.filter(pin__id=post_id, user=user_id).exists():
            return Response({'status': 'exists'})
        else:
            return Response({'status': 'not_exists'})


class ShowAllSavedPin(generic.ListView):
    model = SavedPin
    template_name = 'pintrverse_app/show_all_saved_pins.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        # Add custom filtering or ordering to the queryset
        queryset = queryset.filter(user_id=self.request.user.id)
        return queryset


#
# # FUNCTIONAL BASED FETCH PIN FROM USER's history's keyword
# def fetch_keyword_pin(request):
#     keywords = extract_keywords(get_history_list(5))
#     for keyword in keywords:
#         fetched_tag = Tag.objects.filter(name=str(keyword))
#         break
#     fetched_pin = Pin.objects.filter(tag__id__in=fetched_tag.all())
#     return HttpResponse(fetched_pin)
#
#
# class FetchKeyWordPin(generic.ListView):
#     model = Pin
#     template_name = 'pintrverse_app/fetched_pin.html'
#     keywords = extract_keywords(get_history_list(5))  # function for fetch history & filter keywords from that
#     ls = []
#     for keyword in keywords:
#         if fetched_tag := Tag.objects.filter(name=str(keyword)):  # find TAGS Based on keyword [ history ]
#             for i in fetched_tag.all():
#                 queryset = Pin.objects.filter(tag=i.id)  # Find Pin based on Tag
#                 ls.append(queryset)
#         queryset = []
#         for j in ls:
#             queryset += j


class LikeUnlikePin(generic.View):
    def get(self, request, pin_id):
        pin_obj = Pin.objects.get(id=pin_id)
        if pin_obj.pin_likes and pin_obj.pin_likes.filter(user=request.user.id).exists():
            pin_obj.pin_likes.delete(request.user)
        else:
            pin_obj.pin_likes.add(request.user)
        return redirect(reverse('detail_pin', kwargs={'id': pin_id}))


def search_users(request):
    users = User.objects.all()
    filter = UserFilterSet(request.GET, queryset=users)
    users = filter.qs
    context = {
        'users': users,
        'filter': filter
    }
    return render(request, 'pintrverse_app/search_users.html', context)


def search_pins(request):
    pins = Pin.objects.all()
    filter = PinFilterSet(request.GET, queryset=pins)
    pins = filter.qs
    context = {
        'pins': pins,
        'filter': filter
    }
    return render(request, 'pintrverse_app/search_pins.html', context)


class UpdatePin(generic.UpdateView):
    model = Pin
    fields = ['pin_file', 'title', 'about', 'alt_text', 'destination_link', 'category', 'tag']
    template_name = 'pintrverse_app/pin_update.html'
    success_url = reverse_lazy('home')


class DeletePinView(generic.DeleteView):
    model = Pin
    template_name = 'pintrverse_app/confirm_pin_delete.html'
    success_url = reverse_lazy('home')
