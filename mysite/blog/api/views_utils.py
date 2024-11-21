from rest_framework import viewsets
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from rest_framework.pagination import BasePagination


def get_pagable_response(
    viewset: viewsets.GenericViewSet,
    queryset,
    Serializer: type[Serializer],
    Pagination: type[BasePagination] = None,
):
    paginator = Pagination() if Pagination is not None else viewset.pagination_class()

    page = paginator.paginate_queryset(queryset, viewset.request)
    if page is not None:
        serializer = Serializer(page, many=True, context={"request": viewset.request})
        return paginator.get_paginated_response(serializer.data)

    serializer = Serializer(queryset, many=True, context={"request": viewset.request})
    return Response(serializer.data)
