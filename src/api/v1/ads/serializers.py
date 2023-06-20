from rest_framework import serializers

from ads.models import Ad


class AdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['company', 'title', 'image',]
        extra_kwargs = {
            'title': {'read_only': True},
            'image': {'read_only': True},
        }