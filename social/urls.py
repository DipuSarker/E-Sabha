from django.urls import path, include
from django.views.generic import RedirectView

from .views import HomeView, AboutView, ContactView, MyProfileUpdateView, MyPostCreate, MyPostListView,  MyPostDetailView, MyPostDeleteView, MyProfileListView, MyProfileDetailView, follow, unfollow, like, unlike

urlpatterns = [
    path('home/', HomeView.as_view()),
    path('about/', AboutView.as_view()),
    path('contact/', ContactView.as_view()),
    path('profile/edit/<int:pk>', MyProfileUpdateView.as_view(success_url="/social/home")),

    path('mypost/create', MyPostCreate.as_view(success_url="/social/mypost")),
    path('mypost/delete/<int:pk>', MyPostDeleteView.as_view(success_url="/social/mypost")),
    path('mypost/', MyPostListView.as_view()),
    path('mypost/<int:pk>', MyPostDetailView.as_view()),
    path('mypost/like/<int:pk>', like),
    path('mypost/unlike/<int:pk>', unlike),

    path('myprofile/', MyProfileListView.as_view()),
    path('myprofile/<int:pk>', MyProfileDetailView.as_view()),
    path('myprofile/follow/<int:pk>', follow),
    path('myprofile/unfollow/<int:pk>', unfollow),

    path('', RedirectView.as_view(url='home/'))
]
