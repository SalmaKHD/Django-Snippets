
def CustomFunctionMiddleware(get_response):
    # one-time config or initialization
    print("layer 1 -> one time config")

    def middleware(request):
        # code that is executed before next middleware or view
        print("middleware1 -> before next layer")
        response = get_response(request)
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