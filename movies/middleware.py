from django.http import HttpResponse


def CustomFunctionMiddleware(get_response):
    # one-time config or initialization
    print("layer 1 -> one time config")

    def middleware(request):
        # code that is executed before next middleware or view
        print("middleware1 -> before next layer")
        # return response from URL
        response = HttpResponse("Returning from Middleware Layer 1")
        # response = get_response(request)
        print("middleware 1 -> after next layer")
        # code executed after next layer
        return response
    return middleware

class CustomClassMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print("layer 2 -> one time config")

    def __call__(self, request):
        # code that is executed before next middleware or view
        print("middleware2 -> before next layer")
        # we can do anything we want with the request argument
        response = self.get_response(request)
        print("middleware 2 -> after next layer")
        # code executed after next layer
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        print("Called just before the view")
        print("The HTTP method is: " + request.method)
        print("Name of the called view is:" + view_func.__name__)
        return None

    # def process_exception(self, request, exception):
    #     # may return None or HttpResponse
    #     # has access to the exception raised in view
    #     print(f"Exception raised in {exception}")
    #     return HttpResponse("An Exception occurred!")

    def process_template_response(self, request, response):
        print("Template response called")
        # can change context member values in this hook
        response.context_data['context_from_template_hook'] = "Titanic is among popular movies"
        response.context_data["name"] = "Titanic"
        return response