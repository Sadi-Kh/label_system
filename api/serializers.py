from rest_framework import serializers
from .models import Dataset, Category, TextEntry, Operator
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'dataset', 'is_active', 'labeled_instances_count']


class TextEntrySerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all())
    tagged_by = UserSerializer(read_only=True)

    class Meta:
        model = TextEntry
        fields = ['id', 'content', 'dataset', 'categories', 'tagged_by', 'is_tagged', 'created_at', 'tagged_at']


class DatasetSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    text_entries = TextEntrySerializer(many=True, read_only=True)

    class Meta:
        model = Dataset
        fields = ['id', 'title', 'description', 'categories', 'text_entries', 'total_entries', 'tagged_entries']


class OperatorSerializer(serializers.ModelSerializer):
    datasets = DatasetSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Operator
        fields = ['id', 'user', 'datasets']
