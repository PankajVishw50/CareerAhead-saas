from django.conf import settings

def razorpay_context(request):
    return {
        'razorpay_company_name': "CareerAhead",
        'razorpay_username': settings.RAZORPAY_USERNAME,
    }