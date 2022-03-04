from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


# class ContentListPagination(PageNumberPagination):
#     page_size             = 5
#     page_query_param      = 'p'
#     page_size_query_param = 'size'
#     max_page_size         = 50
#     last_page_strings     = 'end'

# class ContentListPagination(LimitOffsetPagination):
#     default_limit      = 5
#     max_limit          = 10
#     limit_query_param  = 'limit'
#     offset_query_param = 'start'

class ContentListPagination(CursorPagination):
    page_size          = 5
    ordering           = '-avg_rating'
    cursor_query_param = 'record'