from rest_framework import serializers
from taggit.serializers import TagListSerializerField, TaggitSerializer
from django.contrib.auth.models import User
from .models import BlogCategory, BlogPost, Comment, RelatedResource


class BlogCategorySerializer(serializers.ModelSerializer):
    """Serializer for the BlogCategory model."""
    
    class Meta:
        model = BlogCategory
        fields = ['id', 'name', 'description', 'slug', 'icon', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['slug', 'created_at', 'updated_at']


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for blog post authors."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class RelatedResourceSerializer(serializers.ModelSerializer):
    """Serializer for the RelatedResource model."""
    
    class Meta:
        model = RelatedResource
        fields = ['id', 'title', 'description', 'resource_type', 'url', 'file', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class BlogPostSerializer(TaggitSerializer, serializers.ModelSerializer):
    """Serializer for the BlogPost model."""
    category = BlogCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=BlogCategory.objects.all(),
        source='category',
        write_only=True
    )
    author = AuthorSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='author',
        write_only=True
    )
    tags = TagListSerializerField()
    related_resources = RelatedResourceSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'content', 'excerpt', 'featured_image', 
            'category', 'category_id', 'author', 'author_id', 'tags', 
            'is_featured', 'is_published', 'published_date', 'related_resources',
            'comment_count', 'meta_title', 'meta_description', 'created_at', 
            'updated_at'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at', 'comment_count']
    
    def get_comment_count(self, obj):
        """Get the count of approved comments for the blog post."""
        return obj.comments.filter(is_approved=True).count()


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for the Comment model."""
    post = BlogPostSerializer(read_only=True)
    post_id = serializers.PrimaryKeyRelatedField(
        queryset=BlogPost.objects.all(),
        source='post',
        write_only=True
    )
    author_name = serializers.CharField(required=True)
    author_email = serializers.EmailField(required=True)
    
    class Meta:
        model = Comment
        fields = [
            'id', 'post', 'post_id', 'author_name', 'author_email', 'author_website',
            'content', 'is_approved', 'parent', 'created_at', 'updated_at'
        ]
        read_only_fields = ['is_approved', 'created_at', 'updated_at']


class BlogPostDetailSerializer(BlogPostSerializer):
    """Detailed serializer for the BlogPost model including comments."""
    comments = serializers.SerializerMethodField()
    
    class Meta(BlogPostSerializer.Meta):
        fields = BlogPostSerializer.Meta.fields + ['comments']
    
    def get_comments(self, obj):
        """Get approved comments for the blog post."""
        comments = obj.comments.filter(is_approved=True, parent=None)
        return CommentSerializer(comments, many=True).data
