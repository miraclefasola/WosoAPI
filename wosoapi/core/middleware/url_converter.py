from django.urls import path
from api.models import *
from django.shortcuts import redirect
from django.urls import reverse_lazy


class UrlMiddleware:
    def __init__(self, get_response):
        self.get_response=get_response
    def __call__(self, request):
        lower=['wsl', 'uwcl','nwsl']
        others=[ 'arkema', 'frauen']
        twined=['ligaf', 'Ligaf']
        path= request.get_full_path()
        for word in lower:
            if f"/{word}/" in path or path.endswith(f"/{word}"):      
                return redirect(path.replace(word, word.upper()))
        for obj in others:
            if f"/{obj}/" in path or path.endswith(f"/{obj}"):
                return redirect(path.replace(obj, obj.capitalize()))
        for obj in twined:
            if f"/{obj}/" in path or path.endswith(f"/{obj}"):
                return redirect(path.replace(obj, 'LigaF'))
        response= self.get_response(request)
        return response
    
