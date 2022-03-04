from rest_framework.pagination import PageNumberPagination


class ContentListPagination(PageNumberPagination):
    page_size             = 5
    page_query_param      = 'p'
    page_size_query_param = 'size'
    max_page_size         = 50
    last_page_strings     = 'end'