from django.shortcuts import redirect

class JobMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        #urls that require authentication
        protected_urls = [
            "/all-jobs",
            "/job-detail/"
        ]
        # check whether requested url requires login
        for url in protected_urls:
            if request.path.startswith(url):
                if not request.user.is_authenticated:
                    return redirect("login")

        # continue request
        response = self.get_response(request)

        return response