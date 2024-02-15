from product.models import Product

CARD_SESSION_ID = 'card'

class Card:
    def __init__(self, request):
        self.session = request.session
        self.card = self.session.setdefault(CARD_SESSION_ID, {})


    def __iter__(self):
        product_ids = self.card.keys()
        products = Product.objects.filter(id__in = product_ids)
        card = self.card.copy()
        for product in products:
            card[str(product.id)]['product'] = product
            card[str(product.id)]['image'] = product.pic
            card[str(product.id)]['category'] = product.category
        
        for item in card.values():
            item['total_price'] = int(item['price']) * item['quantity']
            yield item

    def add(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.card:
            self.card[product_id] = {'quantity': 0, 'price': str(product.price)}
        self.card[product_id]['quantity'] += quantity
        self.save()

    def update(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.card:
            self.card[product_id] = {'quantity': 0, 'price': str(product.price)}
        self.card[product_id]['quantity'] = quantity
        if quantity <= 0:
            del self.card[product_id]
        self.save()
    
    def delete(self, product):
        product_id = str(product.id)
        del self.card[product_id]
        self.save()


    def save(self):
        self.session.modified = True