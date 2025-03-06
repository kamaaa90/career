from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.BlogCategoryViewSet)
router.register(r'posts', views.BlogPostViewSet)
router.register(r'comments', views.CommentViewSet)

urlpatterns = [
    # Custom endpoints
    path('featured-posts/', views.FeaturedPostsView.as_view(), name='featured-posts'),
    path('posts/by-category/<slug:category_slug>/', views.PostsByCategoryView.as_view(), name='posts-by-category'),
    path('posts/by-tag/<slug:tag_slug>/', views.PostsByTagView.as_view(), name='posts-by-tag'),
    path('posts/<slug:slug>/related/', views.RelatedPostsView.as_view(), name='related-posts'),
]

urlpatterns += router.urls
