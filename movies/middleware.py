
def CustomFunctionMiddleware(get_response):
    # one-time config or initialization
    print("one time")

    def middleware(request):
        # code that is executed before next middleware or view
        print("before next layer")
        response = get_response(request)
        print("after next layer")
        # code executed after next layer
        return response
    return middleware