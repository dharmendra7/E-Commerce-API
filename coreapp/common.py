from django.http import JsonResponse

def send_response(request, message, data):
    response = JsonResponse(data={"message": message,"data":data})
    response.status_code = 200
    return response

def send_response_validation(request, code, message):
    response = JsonResponse(data={"message": message})
    response.status_code = 200
    return response