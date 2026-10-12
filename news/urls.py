"""
URL routing configuration for API endpoints and web views.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from . import api_views, views

router = DefaultRouter()
router.register(r'articles', api_views.ArticleViewSet, basename='article')
router.register(r'newsletters', api_views.NewsletterViewSet, basename='newsletter')  # noqa: E501
router.register(r'publishers', api_views.PublisherViewSet, basename='publisher')  # noqa: E501

urlpatterns = [
    # API Endpoints
    path('api/articles/subscribed/', api_views.subscribed_articles, name='subscribed_articles'),  # noqa: E501
    path('api/approved/', api_views.approved_webhook_receiver, name='approved_webhook'),  # noqa: E501
    path('api/token/', obtain_auth_token, name='api_token_auth'),
    path('api/', include(router.urls)),

    # Front-End UI Views & Dashboards
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),
    path('editor/dashboard/', views.editor_dashbaord, name='editor_dashboard'),
    path('editor/approve/<int:pk>/', views.approve_article, name='approve_article'),  # noqa: E501
    path('journalist/dashboard/', views.journalist_dashboard, name='journalist_dashboard'),  # noqa: E501
    path('reader/subscriptions/', views.manage_subscriptions, name='reader_subscriptions'),  # noqa: E501
    path('publishers/manage/', views.manage_publishers, name='manage_publishers'),  # noqa: E501
]
