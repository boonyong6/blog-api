from rest_framework import viewsets
from rest_framework.serializers import Serializer
from rest_framework.response import Response


def get_pagable_response(
    viewset: viewsets.GenericViewSet, queryset, serializer_type: type[Serializer]
):
    page = viewset.paginate_queryset(queryset)
    if page is not None:
        serializer = serializer_type(
            page, many=True, context={"request": viewset.request}
        )
        return viewset.get_paginated_response(serializer.data)

    serializer = serializer_type(
        queryset, many=True, context={"request": viewset.request}
    )
    return Response(serializer.data)
