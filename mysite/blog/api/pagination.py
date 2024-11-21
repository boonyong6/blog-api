from rest_framework.pagination import PageNumberPagination


class DynamicPageNumberPagination(PageNumberPagination):
    def __init__(self, page_size):
        super().__init__()
        self.page_size = page_size
