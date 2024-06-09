from .models import GameClient

def cart_count(request):
    if request.user.is_authenticated:
        return {
            'cart_count': GameClient.objects.filter(client__user=request.user, in_cart=True).count()
        }
    return {'cart_count': 0}