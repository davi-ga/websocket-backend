from rest_framework.exceptions import AuthenticationFailed

class CurrentUserDefault:

    requires_context = True
    
    def __call__(self, serializer_field):
        user = serializer_field.context.get("request").user
        
        if not user.is_authenticated:
            raise AuthenticationFailed("User is not authenticated")
        
        return user
    
    def __repr__(self):
        return f"{self.__class__.__name__}()"
