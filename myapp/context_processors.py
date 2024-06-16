"""This module include function for cart."""
from .models import GameClient


def cart_count(request):
    """Check that the registered user can add products to the cart.

    Args:
        request: request

    Returns:
        dict with wrong answer
    """
    if request.user.is_authenticated:
        return {
            'cart_count': GameClient.objects.filter(client__user=request.user, in_cart=True).count(),
        }
    return {'cart_count': 0}
