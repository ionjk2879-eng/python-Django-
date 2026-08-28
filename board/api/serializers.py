from rest_framework import serializers

from board.models import Comment, Post


class PostListSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    tag_list = serializers.ReadOnlyField()
    like_count = serializers.IntegerField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    excerpt = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'category', 'tag_list', 'author',
            'view_count', 'like_count', 'comment_count', 'created_at', 'excerpt',
        ]

    def get_excerpt(self, obj):
        return obj.content[:120]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at', 'updated_at']


class PostDetailSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    tag_list = serializers.ReadOnlyField()
    like_count = serializers.IntegerField(read_only=True)
    bookmark_count = serializers.IntegerField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'category', 'tag_list', 'author',
            'view_count', 'like_count', 'bookmark_count', 'comment_count',
            'created_at', 'updated_at',
            'bean_amount', 'water_amount', 'water_temperature', 'brew_time', 'brew_tool',
            'is_liked', 'is_bookmarked',
        ]

    def get_is_liked(self, obj):
        user = self.context['request'].user
        return user.is_authenticated and obj.liked_by.filter(pk=user.pk).exists()

    def get_is_bookmarked(self, obj):
        user = self.context['request'].user
        return user.is_authenticated and obj.bookmarked_by.filter(pk=user.pk).exists()


class PostWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'category', 'tags',
            'bean_amount', 'water_amount', 'water_temperature', 'brew_time', 'brew_tool',
        ]
        read_only_fields = ['id']
