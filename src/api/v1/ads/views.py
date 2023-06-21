from rest_framework import generics, permissions

from ads.models import Ad
from utils.status import AdStatus

from api.v1.ads.serializers import AdsSerializer


class AdListApiView(generics.ListAPIView):
    queryset = Ad.objects.filter(status=AdStatus.ACTIVE)
    permission_classes = (permissions.AllowAny,)
    serializer_class = AdsSerializer