def is_seller_processor(request):
    is_seller = False
    if request.user.is_authenticated:
        is_seller = request.user.groups.filter(name='Seller').exists()
    return {'is_seller': is_seller}