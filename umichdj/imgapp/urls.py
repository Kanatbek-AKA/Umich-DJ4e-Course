from django.urls import path, reverse_lazy
from . import views
from . import models


app_name = 'imgapp'
urlpatterns = [
    # path(route='', view=TemplateView.as_view(template_name="imgapp/list.html"), name='all'),
    path(route='', view=views.AdListView.as_view(), name='all'), 
    path('ad/login/', views.LoginPageView.as_view(), name='login'),       # added
    path('ad/logout/', views.logout_req, name='logout'),                  # added
    path('ad/register/', views.SignupPageView.as_view(), name='signup'),  # added
    # Social oauth pwd
    # path('ad/settings/', views.settings, name='settings'),                # added to test
    # path('ad/settings/password/', views.password, name='password'),       # added to test
    path(route='ad/create', view=views.AdCreateView.as_view(), name='pic_create'), # success_url=reverse_lazy('imgapp:all')
    path(route='ad/<int:pk>', view=views.AdDetailView.as_view(), name='pic_detail'),   
    path(route='ad/<int:pk>/update', view=views.AdUpdateView.as_view(), name='pic_update'),  # success_url=reverse_lazy('pics:all')
    path(route='ad/<int:pk>/delete', view=views.AdDeleteView.as_view(), name='pic_delete'),  #success_url=reverse_lazy('pics:all')
    path(route='ad_picture/<int:pk>', view=views.stream_file, name='pic_picture'),
    # Comment
    path(route='ad/<int:pk>/comment', view=views.CommentCreateView.as_view(), name='ad_comment_create'),
    path(route='ad/comment/<int:pk>/delete', view=views.CommentDeleteView.as_view(), name='ad_comment_delete'),  #success_url=reverse_lazy('ads:all')
    # Favorite 
    path(route='ad/<int:pk>/favorite', view=views.AddFavoriteView.as_view(), name='ad_favorite'),
    path(route='ad/<int:pk>/unfavorite',view=views.DeleteFavoriteView.as_view(), name='ad_unfavorite'),
    # Blog 
    path(route='ad/blog', view=views.BlogListView.as_view(), name='blog'),
    path(route='ad/blog/<int:pk>', view=views.BlogDetailView.as_view(), name='blog_detail'),
    path(route='ad/blog/create/', view=views.BlogCreateView.as_view(), name='blog_create'),
    path(route='ad/blog/<int:pk>/update', view=views.BlogUpdateView.as_view(), name='blog_update'),
    path(route='ad/blog/<int:pk>/delete', view=views.BlogDeleteView.as_view(), name='blog_delete'),

]

