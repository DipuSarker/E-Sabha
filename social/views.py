from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, UpdateView, CreateView, ListView, DetailView, DeleteView
from .models import MyPost, MyProfile, PostLike, PostComment, FollowUser

# Create your views here.
@method_decorator(login_required, name="dispatch")
class HomeView(TemplateView):
    template_name = 'social/home.html'
    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self,**kwargs)
        followedList = FollowUser.objects.filter( followed_by=self.request.user.myprofile)
        followedList2 = []
        for e in followedList:
            followedList2.append(e.profile)
        si = self.request.GET.get('si')
        if si == None:
            si = ''
        postList = MyPost.objects.filter(Q(uploaded_by__in = followedList2)).filter(Q(subject__icontains=si) | Q(msg__icontains=si)).order_by('-id')
        for p1 in postList:
            p1.liked = False
            ob = PostLike.objects.filter(post=p1, liked_by=self.request.user.myprofile)
            if ob:
                p1.liked=True
            ob = PostLike.objects.filter(post=p1)
            p1.likecount = ob.count()
        context['mypost_list'] = postList
        return context

class AboutView(TemplateView):
    template_name = 'social/about.html'



class ContactView(TemplateView):
    template_name = 'social/contact.html'


def follow(request, pk):
    user = MyProfile.objects.get(pk=pk)
    FollowUser.objects.create(profile=user, followed_by=request.user.myprofile)
    return HttpResponseRedirect(redirect_to="/social/myprofile")
def unfollow(request, pk):
    user = MyProfile.objects.get(pk=pk)
    FollowUser.objects.filter(profile=user, followed_by=request.user.myprofile).delete()
    return HttpResponseRedirect(redirect_to="/social/myprofile")


def like(request, pk):
    post = MyPost.objects.get(pk=pk)
    PostLike.objects.create(post=post, liked_by=request.user.myprofile)
    return HttpResponseRedirect(redirect_to="/social/home")
def unlike(request, pk):
    post = MyPost.objects.get(pk=pk)
    PostLike.objects.filter(post=post, liked_by=request.user.myprofile).delete()
    return HttpResponseRedirect(redirect_to="/social/home")




@method_decorator(login_required, name="dispatch")
class MyProfileUpdateView(UpdateView):
    model = MyProfile
    fields = ["name", "age", "address", "status", "gender", "phone_no", "description", "pic"]


@method_decorator(login_required, name="dispatch")
class MyPostCreate(CreateView):
    model = MyPost
    fields = ['subject', 'msg', 'pic']
    def form_valid(self, form):
        self.object = form.save()
        self.object.uploaded_by = self.request.user.myprofile
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())




@method_decorator(login_required, name="dispatch")
class MyPostListView(ListView):
    model = MyPost
    def get_queryset(self):
        si = self.request.GET.get('si')
        if si == None:
            si = ''
        return MyPost.objects.filter(Q(uploaded_by = self.request.user.myprofile)).filter(Q(subject__icontains=si) | Q(msg__icontains=si)).order_by('-id')




@method_decorator(login_required, name="dispatch")
class MyPostDetailView(DetailView):
    model = MyPost
    

@method_decorator(login_required, name="dispatch")
class MyPostDeleteView(DeleteView):
    model = MyPost




@method_decorator(login_required, name='dispatch')
class MyProfileListView(ListView):
    model = MyProfile
    def get_queryset(self):
        si = self.request.GET.get('si')
        if si == None:
            si = ""
        profList = MyProfile.objects.filter(Q(name__icontains = si) | Q(address__icontains = si) | Q(gender__icontains = si) | Q(status__icontains = si)).order_by("-id")
        for p1 in profList:
            p1.followed = False
            ob = FollowUser.objects.filter(profile=p1, followed_by=self.request.user.myprofile)
            if ob:
                p1.followed=True
        return profList

@method_decorator(login_required, name="dispatch")
class MyProfileDetailView(DetailView):
    model = MyProfile



