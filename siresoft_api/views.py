from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["POST"])
def signup(request):
    print(request.headers.items())
    data = request.data
    print(data)

    # if you want to parse plaintext
    # text_data = request.body.decode("utf-8")  # raw bytes → string
    # return Response(f"Received: {text_data}")

    return Response({"message": "User created"})