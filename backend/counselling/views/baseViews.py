from rest_framework import generics

class DecoratorSupportView(generics.GenericAPIView):
    decorators = [lambda: 1 + 1, lambda: 2 + 2]

    def get_queryset(self):
        for decorator in self.decorators:
            pass
