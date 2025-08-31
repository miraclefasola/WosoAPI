from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperUserOrReadOnly(BasePermission):
    message= "You're not allowed to post"
    
    def has_permission(self, request, view):
        # ❌ Block if not logged in
        if not request.user or not request.user.is_authenticated:
            self.message = "You must be logged in to access this resource."
            return False

        # Allow GET for everyone logged in
        if request.method in SAFE_METHODS:
            return True

        # Allow POST/PUT/PATCH/DELETE only for superuser
        if request.method not in SAFE_METHODS:
            
            return request.user.is_superuser

        return False
