from rest_framework import viewsets
from rest_framework.pagination import BasePagination
from rest_framework.response import Response
from rest_framework.serializers import Serializer


def get_pagable_response(
    viewset: viewsets.GenericViewSet,
    queryset,
    serializer_class: type[Serializer],
    pagination_class: type[BasePagination] = None,
):
    # No pagination.
    if viewset.pagination_class is None and pagination_class is None:
        serializer = serializer_class(
            queryset, many=True, context={"request": viewset.request}
        )
        return Response(serializer.data)

    # With pagination.
    paginator = (
        pagination_class()
        if pagination_class is not None
        else viewset.pagination_class()
    )

    page = paginator.paginate_queryset(queryset, viewset.request)
    serializer = serializer_class(page, many=True, context={"request": viewset.request})
    return paginator.get_paginated_response(serializer.data)
