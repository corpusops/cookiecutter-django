from django.contrib.auth import get_user_model


class AutoAuhtMiddleWare(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = get_user_model().objects.all()[0]
        return self.get_response(request)
