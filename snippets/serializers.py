from rest_framework import serializers
from snippets.models import Snippet, CourseList, CoursePage, LANGUAGE_CHOICES, STYLE_CHOICES

from django.contrib.auth.models import User, Group


# class SnippetSerializer(serializers.ModelSerializer):
class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    # highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')
    class Meta:
        model = Snippet
        # fields = ('id', 'title', 'code', 'linenos', 'language', 'style', 'owner')
        fields = ('url', 'id', 'title', 'owner')

class CreateSnippetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    # highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ('url', 'id', 'title', 'code', 'linenos', 'language', 'style', 'owner', 'perm_list')


# class UserSerializer(serializers.ModelSerializer):
class UserSerializer(serializers.HyperlinkedModelSerializer):
    # snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'snippets')


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.groups.add(1)
        user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password','email', 'first_name', 'last_name',)


class CreateCourseSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = CourseList
        fields = ( 'title', 'descrpt', 'owner')


class CreateCoursePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoursePage
        fields = ('course', 'snippet', 'order', 'dtm')


class CourseListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CourseList
        fields = ( 'url', 'id','title', 'descrpt', 'owner')


class CourseDetailSerializer(serializers.HyperlinkedModelSerializer):
    # pages = serializers.StringRelatedField(many=True)
    pages = serializers.HyperlinkedRelatedField(many=True, view_name = 'coursepage-detail', read_only=True)

    class Meta:
        model = CourseList
        fields = ('title', 'descrpt', 'pages')


class CoursePageSerializer(serializers.HyperlinkedModelSerializer):
    # snippet = serializers.HyperlinkedRelatedField(many=False, view_name='snippet-detail', read_only=True)
    class Meta:
        model = CoursePage
        fields = ('url','order', 'course', 'snippet')


class CourseDetailPageSerializer(serializers.HyperlinkedModelSerializer):
    # pages = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)
    title = serializers.ReadOnlyField(source='snippet.title')

    class Meta:
        model = CoursePage
        fields = ('title','snippet')
