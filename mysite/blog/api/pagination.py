from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class DynamicPageNumberPagination(PageNumberPagination):
    def __init__(self, page_size=None):
        super().__init__()
        if page_size is not None:
            self.page_size = page_size

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "page_size": self.page_size,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )
