from .upload import handler as upload_handler
from .view import handler as view_handler

def handler(request, response):
    if request.path == "/api/upload":
        return upload_handler(request, response)
    if request.path == "/api/view":
        return view_handler(request, response)
    
    response.status = 404
    return response.json({"error": "Not Found"})
