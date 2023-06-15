from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse, resolve
from django.utils.http import urlencode
from django.http import HttpResponse
# Views 
from django.views.generic import ListView, DetailView, TemplateView, DeleteView, UpdateView 
from django.views import View
# Local models, forms
from .models import Ad, Comment, Fav, Blog
from .form import CreateForm, CommentForm, BlogForm
# 
from django.conf import settings
# Decors, tokens  
from django.db.utils import IntegrityError                       # <<--  
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.decorators import method_decorator             # <<-- 
# Social Oauth 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from social_django.models import UserSocialAuth
from social_core.pipeline.partial import partial
from social_core.exceptions import AuthAlreadyAssociated, AuthException, AuthForbidden
# Another way social oauth
from authlib.integrations.django_client import OAuth
from urllib.parse import quote_plus, urlencode
import json
# Search
from django.db.models import Q
from django.contrib.humanize.templatetags.humanize import naturaltime
# 
import logging
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

# TODO 
from django.utils.html import conditional_escape, escape, mark_safe

# Clear cache TODO
from django.core.cache import cache
# from django.forms.renderers import TemplatesSetting


# TODO modify logger
logger = logging.getLogger(__name__)



class LoginPageView(View):
    template_name = "imgapp/login.html"
    extra_context = {"settings": settings}

    def get(self, request):
        return render(request, self.template_name, {
            "session": request.session.get("user"), 
            "pretty": json.dumps(request.session.get("user"), indent=4),
            })

    def post(self, request): 
        name = request.POST['username']
        pwd = request.POST['pwd']
        user = authenticate(username=name, password=pwd)
        if user is not None:
            login(request, user)
            return redirect("imgapp:all")

        # This way did not get point yet 
        # loginurl = reverse('imgapp:login')+'?'+urlencode({'next': request.path})
        # return redirect(loginurl)

        return render(request, self.template_name, {"warning": "User does not exist, Plaese, sign up!"})


def logout_req(request):
    logout(request)
    return redirect("imgapp:all")


class SignupPageView(View):
    model = User
    template_name = 'imgapp/signup.html'
    # success_url = reverse_lazy("imgapp:all") 

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        name = request.POST['username']
        password = request.POST['pwd']
        email = request.POST['email']
        user_exist = False
        try:
            User.objects.get(username=name)
            user_exist = True
        except :
            logger.error("New User")

        if not user_exist:
            new_user = User.objects.create_user(
                username = name,
                password = password,
                email = email,
                )
            login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')  # otherwise settings.AUTHENTICATION_BACKENDS[index]
            return redirect("imgapp:all")
        else:
            return render(request, self.template_name, {'warning': 'This nickname already exists, would you not mind to choose other nickname!'})

        return render(request, self.template_name, {})    



# in extra content add some python functions like you location, device, ip, time, date
class AdListView(ListView):
    model = Ad
    template_name = "imgapp/list.html"
    # content_type = 
    # extra_context = {}
    success_url = reverse_lazy('imgapp:all')

    def get(self, request): 
        favorites = []
        # ad = Ad.objects.all()
        srch = request.GET.get("imsearch", False)
        
        if request.user.is_authenticated:
            rows = request.user.favorite_ads.values('id')                # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
            favorites = [ row['id'] for row in rows ]                   # favorites = [2, 4, ...] using list comprehension
        
        if srch:
            query = Q(title__icontains=srch)
            query.add(Q(text__icontains=srch), Q.OR)
            query.add(Q(tags__name__in=[srch]), Q.OR)
            add_list = Ad.objects.filter(query).select_related().distinct().order_by('-updated_at')[:10]
        else: 
            add_list = Ad.objects.all().order_by('-updated_at')[:10]
        for obj in add_list:
            obj.natural_updated = naturaltime(obj.updated_at)

        return render(request, self.template_name, {'ad': add_list, 'favorites': favorites, "search": srch})



class AdDetailView(LoginRequiredMixin, DetailView):
    model = Ad
    template_name = "imgapp/detail.html"
    success_url = reverse_lazy('imgapp:pic_detail')

    def get(self, request, pk) :
        mod = Ad.objects.get(id=pk)
        comments = Comment.objects.filter(ad=mod).order_by('-updated_at')
        comment_form = CommentForm()
        return render(request, self.template_name, {"ad":mod, 'comments': comments, 'comment_form': comment_form } )


class AdCreateView(LoginRequiredMixin, View): 
    login_url = "login/"                         #<<----
    template_name = 'imgapp/forms.html'
    success_url = reverse_lazy('imgapp:all')             

    def get(self, request, pk=None):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)
        # Add owner to the model before saving
        pic = form.save(commit=False)
        pic.owner = self.request.user
        pic.save()
        
        return redirect(self.success_url)


class AdUpdateView(LoginRequiredMixin ,UpdateView): # 
    template_name = 'imgapp/forms.html'
    success_url = reverse_lazy('imgapp:all')

    def get(self, request, pk):
        pic = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(instance=pic)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        pic = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=pic)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)
        pic = form.save(commit=False)
        pic.save()

        return redirect(self.success_url)


class AdDeleteView(LoginRequiredMixin, DeleteView):
    model = Ad
    template_name = "imgapp/delete.html"
    success_url = reverse_lazy('imgapp:all')

    def get_queryset(self):
        user = self.request.user
        qs = super(AdDeleteView, self).get_queryset()   
        return qs.filter(owner=user)



class BlogListView(LoginRequiredMixin, ListView):
    model = Blog
    template_name = "imgapp/blog.html"
    # content_type = 
    # extra_context = {}

    def get(self, request): 
        srch = request.GET.get("bsearch", False)
        if srch:
            query = Q(title__icontains= srch)
            query.add(Q(text__icontains=srch), Q.OR)
            query.add(Q(tags__name__in=[srch]), Q.OR)
            blog_list = Blog.objects.filter(query).select_related().distinct().order_by('-updated_at')[:10]
        else: 
            blog_list = Blog.objects.all().order_by('-updated_at')[:10]

        # skipped 
        for obj in blog_list:
            obj.natural_updated = naturaltime(obj.updated_at)

        return render(request, self.template_name, {"blog": blog_list, "search": srch} )


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog
    template_name = "imgapp/blog_detail.html"
    # success_url = reverse_lazy('imgapp:blog_detail')

    def get(self, request, pk) :
        blog = Blog.objects.get(id=pk)
        return render(request, self.template_name, {"blog":blog} )


class BlogCreateView(LoginRequiredMixin, View):
    model = Blog 
    template_name = "imgapp/bform.html" 
    login_url = "login/"                         
    success_url = reverse_lazy('imgapp:blog')             

    def get(self, request, pk=None):
        blog = BlogForm()
        ctx = {'blog': blog}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        blog = BlogForm(request.POST)
        if not blog.is_valid():
            ctx = {'blog': blog}
            return render(request, self.template_name, ctx)

        art = blog.save(commit=False)
        art.owner = self.request.user
        blog.save()
        return redirect(self.success_url)


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    template_name = "imgapp/bform.html"
    success_url=reverse_lazy('imgapp:blog')

    def get(self, request, pk):
        blog = get_object_or_404(Blog, id=pk, owner=self.request.user)
        form = BlogForm(instance=blog)
        return render(request, self.template_name, {'blog': form})

    def post(self, request, pk=None):
        blog = get_object_or_404(Blog, id=pk, owner=self.request.user)
        form = BlogForm(request.POST, instance=blog)
        if not form.is_valid():
            return render(request, self.template_name, {'blog': form})

        art = form.save(commit=False)
        art.save()
        return redirect(self.success_url)


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog 
    template_name = "imgapp/bdelete.html"
    success_url=reverse_lazy('imgapp:blog') 

    def get_queryset(self):
        user = self.request.user
        qs = super(BlogDeleteView, self).get_queryset()   
        return qs.filter(owner=user)



# @method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    # model = Fav
    success_url = reverse_lazy("imgapp:all")

    def post(self, request, pk) :
        ad = get_object_or_404(Ad, id=pk)
        fav = Fav(user=request.user, ad=ad)
        try:
            fav.save()                 # In case of duplicate key
        except IntegrityError as e:
            pass
        return redirect(self.success_url)


# @method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    success_url = reverse_lazy("imgapp:all")
  
    def post(self, request, pk) :
        # print("Delete PK",pk)
        ad = get_object_or_404(Ad, id=pk)
        try:
            fav = Fav.objects.get(user=request.user, ad=ad).delete()
        except Fav.DoesNotExist as e:
            pass
        return redirect(self.success_url)



class CommentCreateView(LoginRequiredMixin, View):
    model = Comment
    template_name = "imgapp/comments.html"
    # success_url = reverse_lazy("imgapp:pic_detail")

    def get(self, request, pk=None):
        commentForm = CommentForm()
        return render(request, self.template_name, {"comments": commentForm})

    def post(self, request, pk):
        ad = get_object_or_404(Ad, id=pk)
        form = Comment(text=request.POST['comment'], owner=request.user, ad=ad)
        form.save()
        return redirect(reverse("imgapp:pic_detail", args=[pk]))


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "imgapp/cdelete.html"
    success_url=reverse_lazy('imgapp:pic_detail')

    def get_success_url(self):
        comment = self.object.ad
        return reverse('imgapp:pic_detail', args=[comment.id])



def stream_file(request, pk):
    pic = get_object_or_404(Ad, id=pk)
    response = HttpResponse()
    response['Content-Type'] = pic.content_type
    response['Content-Length'] = len(pic.picture)
    response.write(pic.picture)
    return response

