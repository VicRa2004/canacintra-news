from django.urls import path
from .views import NewsListView, NewsDetailView, add_comment, SignUpView

urlpatterns = [
    path('', NewsListView.as_view(), name='news_list'),
    path('news/<slug:slug>/', NewsDetailView.as_view(), name='news_detail'),
    path('news/<int:pk>/comment/', add_comment, name='add_comment'),
    path('signup/', SignUpView.as_view(), name='signup'),
]
