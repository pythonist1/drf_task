from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import PostSerializer, CommentSerializer
from .models import Post, Comment
# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('heading')
    serializer_class = PostSerializer


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes((IsAuthenticated,))
def posts_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        
        heading = request.query_params.get('heading', None)
        if heading is not None:
            posts = posts.filter(heading__icontains=heading)
        
        serializer = PostSerializer(posts, many=True)
        for data in serializer.data:
            data['comments'] = []
            post_object = Post.objects.get(pk=data['id'])
            for comment in post_object.comment_set.all():
                data['comments'].append({'date': comment.date, 'text': comment.text, 'id': comment.id})
        return Response(serializer.data)
 
    elif request.method == 'POST':
        post_data = JSONParser().parse(request)
        serializer = PostSerializer(data=post_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        count = Post.objects.all().delete()
        return Response({'message': '{} Tutorials were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
 
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def posts_detail(request, pk):
    try: 
        post = Post.objects.get(pk=pk) 
    except Post.DoesNotExist: 
        return Response({'message': 'The post does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        serializer = PostSerializer([post], many=True)
        for data in serializer.data:
            data['comments'] = []
            for comment in post.comment_set.all():
                data['comments'].append({'date': comment.date, 'text': comment.text, 'id': comment.id})
        return Response(serializer.data[0]) 
 
    elif request.method == 'PUT': 
        post_data = JSONParser().parse(request) 
        serializer = PostSerializer(post, data=post_data) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        post.delete() 
        return Response({'message': 'Post was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def comment_detail(request, pk=None):
    try: 
        comment = Comment.objects.get(pk=pk) 
    except Comment.DoesNotExist: 
        return Response({'message': 'The comment does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        serializer = CommentSerializer(comment)
        return Response(serializer.data) 

    elif request.method == 'POST':
        comment_data = JSONParser().parse(request)
        serializer = CommentSerializer(data=comment_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
         
    elif request.method == 'PUT': 
        comment_data = JSONParser().parse(request) 
        serializer = CommentSerializer(comment, data=comment_data) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        comment.delete() 
        return Response({'message': 'Comment was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def token_identificate(request):
    token = JSONParser().parse(request)
    try:
        token, created = Token.objects.get_or_create(key=token['token'])
        user = User.objects.get(pk=token.user_id)
        return Response({'username':user.username})
    except Exception as exp:
        print(exp)
        return Response({'message': 'Token does not exist'}, status=status.HTTP_404_NOT_FOUND)

# POST request {'token': 'user token'}