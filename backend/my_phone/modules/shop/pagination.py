from rest_framework.pagination import PageNumberPagination


class PhonePagination(PageNumberPagination):
    """
    手机列表分页
    """
    page_query_param = "page"
    page_size_query_param = "size"
    page_size = 5
    max_page_size = 10
