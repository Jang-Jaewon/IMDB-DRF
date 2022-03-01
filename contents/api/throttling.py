from rest_framework.throttling  import UserRateThrottle


class ReviewCreateThrotlling(UserRateThrottle):
    scope = 'review-create'


class ReviewListThrotlling(UserRateThrottle):
    scope = 'review-list'