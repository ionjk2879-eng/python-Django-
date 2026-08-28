from django.db.models import Count, F, Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from board.models import Comment, Post

from .permissions import IsAuthorOrReadOnly
from .serializers import CommentSerializer, PostDetailSerializer, PostListSerializer, PostWriteSerializer


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        queryset = Post.objects.select_related('author').annotate(
            like_count=Count('liked_by', distinct=True),
            bookmark_count=Count('bookmarked_by', distinct=True),
            comment_count=Count('comments', distinct=True),
        ).order_by('-created_at')

        query = self.request.query_params.get('q', '').strip()
        search_type = self.request.query_params.get('type', 'all')
        category = self.request.query_params.get('category', '').strip()
        if category in Post.Category.values:
            queryset = queryset.filter(category=category)
        if not query:
            return queryset

        if search_type == 'title':
            condition = Q(title__icontains=query)
        elif search_type == 'content':
            condition = Q(content__icontains=query)
        elif search_type == 'author':
            condition = Q(author__username__icontains=query)
        else:
            condition = (
                Q(title__icontains=query)
                | Q(content__icontains=query)
                | Q(author__username__icontains=query)
                | Q(tags__icontains=query)
            )
        return queryset.filter(condition)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PostDetailSerializer
        if self.action in ('create', 'update', 'partial_update'):
            return PostWriteSerializer
        return PostListSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        Post.objects.filter(pk=instance.pk).update(view_count=F('view_count') + 1)
        instance.refresh_from_db(fields=['view_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def recommendations(self, request, pk=None):
        post = self.get_object()
        queryset = self.get_queryset().filter(category=post.category).exclude(pk=post.pk)
        queryset = queryset.order_by('-like_count', '-view_count')[:5]
        serializer = PostListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        return self._toggle_reaction(request, 'liked_by')

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def bookmark(self, request, pk=None):
        return self._toggle_reaction(request, 'bookmarked_by')

    def _toggle_reaction(self, request, field_name):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        relation = getattr(post, field_name)
        active = relation.filter(pk=request.user.pk).exists()
        if active:
            relation.remove(request.user)
        else:
            relation.add(request.user)
        return Response({'active': not active, 'count': relation.count()})


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        queryset = Comment.objects.select_related('author').order_by('created_at')
        post_id = self.request.query_params.get('post')
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
