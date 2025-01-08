from django.conf import settings

from util.response import ErrorResponseTemplates

def get_pagination_params(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            page = int(request.GET.get('page', 1))
            size = int(request.GET.get('size', settings.PAGE_SIZE))



        except ValueError:
            return ErrorResponseTemplates.BAD_REQUEST('Invalid payload. `page` and `size` must be valid integer.')
        except:
            page = 1
            size = settings.PAGE_SIZE

        # Validation
        # - page validation
        if page < 1:
            return ErrorResponseTemplates.BAD_REQUEST("Page must be an positive integer")
        # - size validation
        if size < 1 or size > settings.MAX_PAGE_SIZE:
            return ErrorResponseTemplates.BAD_REQUEST(f"Invalid size: size must be 0 < size <= {settings.MAX_PAGE_SIZE}")

                      
        request.pagination = PaginationParams(page, size)
        return func(self, request, *args, **kwargs)
    return wrapper

class PaginationParams:
    def __init__(self, page, size):
        self.page = page 
        self.size = size  
