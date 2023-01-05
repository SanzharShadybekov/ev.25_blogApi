from rest_framework import serializers
from .models import Category, Post, Comment, PostImages


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImages
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    # owner = serializers.PrimaryKeyRelatedField(read_only=True)
    owner = serializers.ReadOnlyField(source='owner.id')
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Comment
        fields = '__all__'


class PostDetailSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    category_name = serializers.ReadOnlyField(source='category.name')
    # images = PostImageSerializer(many=True) # 2ой способ
    # comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['comments_count'] = instance.comments.count()
        rep['comments'] = CommentSerializer(instance.comments.all(),
                                            many=True).data
        rep['images'] = PostImageSerializer(instance.images.all(),
                                            many=True).data # 1ый способ
        # rep['comments_count'] = len(rep['comments'])
        return rep


class PostListSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Post
        fields = ('id', 'title', 'owner', 'owner_username',
                  'category', 'category_name', 'preview')


class PostCreateSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, read_only=False, required=False)

    class Meta:
        model = Post
        fields = ('title', 'body', 'category', 'preview', 'images')

    def create(self, validated_data):
        # print(self, '!!!!!!!!!!!!!')
        print(validated_data, '-----------------')
        request = self.context.get('request')
        post = Post.objects.create(**validated_data)
        # print(request.FILES.getlist('images'), '!!!!!!!!!!!!!!!!!!!!')
        images_data = request.FILES.getlist('images')
        for image in images_data:
            PostImages.objects.create(image=image, post=post)
        return post






