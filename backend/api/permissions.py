from rest_framework.permissions import BasePermission, SAFE_METHODS

class AllowFormGetAndSubmitOnly(BasePermission):
    def has_permission(self, request, view):
        basename = getattr(view, 'basename', None)
        print(basename)
        if basename == 'form' and request.method in SAFE_METHODS:
            return True
        
        if basename == 'formanwser' and request.method == 'POST':
            return True
        
        return request.user and request.user.is_authenticated