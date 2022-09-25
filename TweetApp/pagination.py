from rest_framework.pagination import PageNumberPagination


class TweetPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = "page"
