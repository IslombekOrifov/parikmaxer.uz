from rest_framework import serializers

from ads.models import Ad


class AdsAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = "__all__"
        extra_kwargs = {
            'author': {'read_only': True},
        }


class AdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['title', 'image',]
        extra_kwargs = {
            'title': {'read_only': True},
            'image': {'read_only': True},
        }