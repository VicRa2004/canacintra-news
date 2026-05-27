from django.urls import path
from .views import (
    NewsListView, NewsDetailView, add_comment, SignUpView,
    DashboardHomeView, DashboardNewsCreateView, DashboardNewsUpdateView, DashboardNewsDeleteView,
    approve_comment_api, delete_comment_api, create_category_api
)

urlpatterns = [
    path('', NewsListView.as_view(), name='news_list'),
    path('news/<slug:slug>/', NewsDetailView.as_view(), name='news_detail'),
    path('news/<int:pk>/comment/', add_comment, name='add_comment'),
    path('signup/', SignUpView.as_view(), name='signup'),
    
    # Dashboard Paths
    path('dashboard/', DashboardHomeView.as_view(), name='dashboard_home'),
    path('dashboard/news/create/', DashboardNewsCreateView.as_view(), name='dashboard_news_create'),
    path('dashboard/news/<int:pk>/edit/', DashboardNewsUpdateView.as_view(), name='dashboard_news_edit'),
    path('dashboard/news/<int:pk>/delete/', DashboardNewsDeleteView.as_view(), name='dashboard_news_delete'),
    
    # Dashboard API AJAX
    path('dashboard/api/comment/<int:pk>/approve/', approve_comment_api, name='approve_comment_api'),
    path('dashboard/api/comment/<int:pk>/delete/', delete_comment_api, name='delete_comment_api'),
    path('dashboard/api/category/create/', create_category_api, name='create_category_api'),
]
