import json
import sys

from django.contrib.auth.models import User
from django.db.models import Count
from django.http import Http404
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, Like, UserInfo
from .serializers import PostSerializer, UserSerializer, UserInfoSerializer, LikeSerializer, LikeAnalyticsSerializer


class PostView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = Post.objects.filter(id=request.GET.get("id")) \
            if "id" in request.GET.keys() and request.GET.get("id") != "" \
            else Post.objects.all()
        return Response(PostSerializer(instance=queryset, many=True).data)

    def post(self, request):
        post = Post(
            title=request.data["title"],
            body=request.data["body"],
            author=User.objects.get(id=self.request.user.id),
        )
        post.clean()
        post.save()
        return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)

    def put(self, request):
        post = Post.objects.get(id=request.GET.get("id"))
        post.title = request.data["title"]
        post.body = request.data["body"]
        post.clean()
        post.save()
        return Response(PostSerializer(post).data)

    def delete(self, request):
        Post.objects.get(id=request.GET.get("id")).delete()
        return Response()


class UserNewView(CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserInfoView(APIView):
    def get(self, request):
        try:
            info = {
                "last_login": User.objects.get(id=request.GET.get("user_id")).last_login,
                "last_request": UserInfo.objects.get(user=request.GET.get("user_id")).last_request,
            }
            return Response(UserInfoSerializer(info).data)
        except UserInfo.DoesNotExist:
            raise Http404()


class LikeView(APIView):
    def get(self, request):
        queryset = Like.objects.filter(
            date__range=[f"{request.GET.get('date_from')} 00:00Z", f"{request.GET.get('date_to')} 00:00Z"],
            like=1
        )
        if "post_id" in request.GET.keys() and request.GET.get("post_id") != "":
            queryset = queryset.filter(post_id=request.GET.get("post_id"))
        if "user_id" in request.GET.keys() and request.GET.get("user_id") != "":
            queryset = queryset.filter(user_id=request.GET.get("user_id"))
        data = queryset.values("date__date").annotate(count=Count('date__date'))
        print(data, file=sys.stderr)
        return Response(LikeAnalyticsSerializer(instance=data, many=True).data)


    def put(self, request):
        like_obj, _ = Like.objects.get_or_create(
            post=Post.objects.get(id=request.GET.get("post_id")),
            user=User.objects.get(id=self.request.user.id),
            defaults={"like": 0}
        )
        like_obj.like = 1 if like_obj.like == 0 else 0
        like_obj.save()

        return Response(LikeSerializer(like_obj).data)


class RootView(APIView):
    def get(self, request):
        response = {"description": "This is SocialNetworkAPI. "
                                   "Detailed info on https://documenter.getpostman.com/view/18156181/UVC6jmpa"}
        return Response(data=json.dumps(response))
