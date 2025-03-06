from django.db.models import Q, Count
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from .models import BlogCategory, BlogPost, Comment, RelatedResource
from .serializers import (
    BlogCategorySerializer, BlogPostSerializer, CommentSerializer,
    RelatedResourceSerializer, BlogPostDetailSerializer
)


class BlogCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for the BlogCategory model."""
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    lookup_field = 'slug'
    
    def get_permissions(self):
        """Set permissions based on action."""
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """Filter queryset based on user permissions."""
        queryset = BlogCategory.objects.all()
        
        # Filter active categories for non-admin users
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
            
        return queryset


class BlogPostViewSet(viewsets.ModelViewSet):
    """ViewSet for the BlogPost model."""
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'
    
    def get_permissions(self):
        """Set permissions based on action."""
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """Filter queryset based on user permissions and query parameters."""
        queryset = BlogPost.objects.all()
        
        # Filter published posts for non-admin users
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_published=True)
        
        # Filter by category
        category_slug = self.request.query_params.get('category', None)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Filter by tag
        tag = self.request.query_params.get('tag', None)
        if tag:
            queryset = queryset.filter(tags__name__in=[tag])
        
        # Search by title or content
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(content__icontains=search) |
                Q(excerpt__icontains=search)
            )
            
        return queryset
    
    def get_serializer_class(self):
        """Return different serializer for detail view."""
        if self.action == 'retrieve':
            return BlogPostDetailSerializer
        return super().get_serializer_class()
    
    @action(detail=True, methods=['get'])
    def comments(self, request, slug=None):
        """Get approved comments for a blog post."""
        post = self.get_object()
        comments = post.comments.filter(is_approved=True, parent=None)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def related_resources(self, request, slug=None):
        """Get related resources for a blog post."""
        post = self.get_object()
        resources = post.related_resources.all()
        serializer = RelatedResourceSerializer(resources, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for the Comment model."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def get_permissions(self):
        """Set permissions based on action."""
        if self.action in ['create']:
            permission_classes = [AllowAny]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """Filter queryset based on user permissions."""
        queryset = Comment.objects.all()
        
        # Filter approved comments for non-admin users
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_approved=True)
        
        # Filter by post
        post_slug = self.request.query_params.get('post', None)
        if post_slug:
            queryset = queryset.filter(post__slug=post_slug)
            
        return queryset
    
    def perform_create(self, serializer):
        """Set is_approved to False for new comments."""
        serializer.save(is_approved=False)


class FeaturedPostsView(APIView):
    """View for getting featured blog posts."""
    permission_classes = [AllowAny]
    
    def get(self, request):
        posts = BlogPost.objects.filter(is_featured=True, is_published=True)
        serializer = BlogPostSerializer(posts, many=True)
        return Response(serializer.data)


class PostsByCategoryView(APIView):
    """View for getting blog posts by category."""
    permission_classes = [AllowAny]
    
    def get(self, request, category_slug):
        category = get_object_or_404(BlogCategory, slug=category_slug, is_active=True)
        posts = BlogPost.objects.filter(category=category, is_published=True)
        serializer = BlogPostSerializer(posts, many=True)
        return Response(serializer.data)


class PostsByTagView(APIView):
    """View for getting blog posts by tag."""
    permission_classes = [AllowAny]
    
    def get(self, request, tag_slug):
        posts = BlogPost.objects.filter(tags__slug=tag_slug, is_published=True)
        serializer = BlogPostSerializer(posts, many=True)
        return Response(serializer.data)


class RelatedPostsView(APIView):
    """View for getting related blog posts."""
    permission_classes = [AllowAny]
    
    def get(self, request, slug):
        post = get_object_or_404(BlogPost, slug=slug, is_published=True)
        
        # Get posts with the same category or tags
        related_posts = BlogPost.objects.filter(
            Q(category=post.category) | Q(tags__in=post.tags.all())
        ).exclude(id=post.id).distinct().filter(is_published=True)[:5]
        
        serializer = BlogPostSerializer(related_posts, many=True)
        return Response(serializer.data)
