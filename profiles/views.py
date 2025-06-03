from rest_flex_fields.views import FlexFieldsMixin
from djoser.views import UserViewSet as DjoserUserViewSet


class UserViewSet(FlexFieldsMixin, DjoserUserViewSet):
    def get_queryset(self):
        queryset = super().get_queryset().distinct()
        return queryset


