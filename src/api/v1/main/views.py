from rest_framework import (
    generics, 
    permissions,
    response,
    validators
)

from utils.status import Status1
from main.models import (
    News,
)

from api.v1.main.serializers import (
    NewsSerializer,
)



class NewsListAPIView(generics.ListAPIView):
    queryset = News.objects.filter(status=Status1.ACTIVE)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = NewsSerializer
