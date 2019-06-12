from django.shortcuts import render



from snippets.models import Snippet, CourseList, CoursePage
from django.contrib.auth.models import User
from snippets.serializers import SnippetSerializer, UserSerializer,\
    UserCreateSerializer, CreateSnippetSerializer, CreateCourseSerializer,\
    CreateCoursePageSerializer, CourseDetailSerializer, CourseListSerializer,\
    CoursePageSerializer, CourseDetailPageSerializer

from rest_framework import generics
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly, IfGroup2


class SnippetList(generics.ListAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.DjangoModelPermissions,)


class CreateSnippet(generics.CreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = CreateSnippetSerializer
    permission_classes = (permissions.DjangoModelPermissions,)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = CreateSnippetSerializer
    permission_classes = (permissions.DjangoModelPermissions, IsOwnerOrReadOnly, IfGroup2)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.DjangoModelPermissions, IsOwnerOrReadOnly)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.DjangoModelPermissions,)


class CreateUserView(generics.CreateAPIView):
    model = User
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserCreateSerializer


class CreateCourseView(generics.ListCreateAPIView):
    queryset = CourseList.objects.all()
    serializer_class = CreateCourseSerializer
    permission_classes = (permissions.DjangoModelPermissions,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CreatePageView(generics.ListCreateAPIView):
    queryset = CoursePage.objects.all()
    serializer_class = CreateCoursePageSerializer
    permission_classes = (permissions.DjangoModelPermissions,)


class CoursListView(generics.ListAPIView):
    queryset = CourseList.objects.all()
    serializer_class = CourseListSerializer
    permission_classes = (permissions.DjangoModelPermissions,)


class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CourseList.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = (permissions.DjangoModelPermissions, IsOwnerOrReadOnly,)


class CoursPageListView(generics.ListAPIView):
    queryset = CoursePage.objects.all()
    serializer_class = CoursePageSerializer
    permission_classes = (permissions.DjangoModelPermissions,)


class CoursPageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CoursePage.objects.all()
    serializer_class = CourseDetailPageSerializer
    permission_classes = (permissions.DjangoModelPermissions,)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        # 'users': reverse('user-list', request=request, format=format),
        # 'snippets': reverse('snippet-list', request=request, format=format),
        'courses': reverse('courselist-list', request=request, format=format),
        'registration': reverse('user-list', request=request, format=format)
    })


# ~ class SnippetHighlight(generics.GenericAPIView):
    # ~ queryset = Snippet.objects.all()
    # ~ renderer_classes = (renderers.StaticHTMLRenderer,)

    # ~ def get(self, request, *args, **kwargs):
        # ~ snippet = self.get_object()
        # ~ return Response(snippet.highlighted)
