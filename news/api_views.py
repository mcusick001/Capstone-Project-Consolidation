"""
API ViewSets and endpoints for DRF serialization
and custom filtering.
"""

from django.db import models
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Article, Publisher, Newsletter
from .serializers import ArticleSerializer, PublisherSerializer, NewsletterSerializer  # noqa: E501
from .permissions import IsJournalistCanCreateOrEditorCanApprove


class ArticleViewSet(viewsets.ModelViewSet):
    """API endpoint for managing articles with
    RBAC enforcement."""
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsJournalistCanCreateOrEditorCanApprove]

    def perform_create(self, serializer):
        serializer.save(journalist=self.request.user, approved=False)


class PublisherViewSet(viewsets.ModelViewSet):
    """API endpoint for publisher management."""
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class NewsletterViewSet(viewsets.ModelViewSet):
    """API endpoint for newsletter aggregation."""
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def subscribed_articles(request):
    """Returns approved articles matching the authenticated
    reader's subscriptions."""
    user = request.user
    pubs = user.subscriptions_publishers.all()
    jours = user.subscriptions_journalists.all()

    articles = Article.objects.filter(approved=True).filter(
            models.Q(publisher__in=pubs) | models.Q(journalist__in=jours)
    ).distinct()

    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def approved_webhook_receiver(request):
    """Internal webhook receiver endpoint for article
    approval events."""
    return Response({"status": "received", "data": request.data}, status=status.HTTP_200_OK)  # noqa: E501
