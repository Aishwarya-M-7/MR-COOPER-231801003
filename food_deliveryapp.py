# -------------------- MenuItem --------------------
class MenuItem:
    def __init__(self, item_id, name, price, category, is_available=True, preparation_time=10):
        self.item_id = item_id
        self.name = name
        self.price = price
        self.category = category
        self.is_available = is_available
        self.preparation_time = preparation_time

    def update_price(self, new_price):
        self.price = new_price

    def mark_unavailable(self):
        self.is_available = False

    def __str__(self):
        return f"{self.name} - Rs {self.price}"


# -------------------- Restaurant --------------------
class Restaurant:
    def __init__(self, restaurant_id, name, cuisine, rating=0.0, is_open=True):
        self.restaurant_id = restaurant_id
        self.name = name
        self.cuisine = cuisine
        self.menu = []
        self.rating = rating
        self.is_open = is_open

    def add_menu_item(self, item):
        self.menu.append(item)

    def remove_menu_item(self, item_id):
        self.menu = [i for i in self.menu if i.item_id != item_id]

    def accept_order(self):
        return self.is_open

    def reject_order(self):
        return not self.is_open


# -------------------- Cart --------------------
class Cart:
    def __init__(self, cart_id, customer_id):
        self.cart_id = cart_id
        self.customer_id = customer_id
        self.items = []
        self.promo_code = None

    def add_item(self, item):
        if item.is_available:
            self.items.append(item)
        else:
            print("Item not available")

    def remove_item(self, item_id):
        self.items = [i for i in self.items if i.item_id != item_id]

    def apply_promo(self, code):
        self.promo_code = code

    def checkout(self):
        total = sum(i.price for i in self.items)

        if self.promo_code == "DISCOUNT10":
            total *= 0.9

        return total


# -------------------- DeliveryPartner --------------------
class DeliveryPartner:
    def __init__(self, partner_id, name, phone, location, rating=0.0):
        self.partner_id = partner_id
        self.name = name
        self.phone = phone
        self.location = location
        self.is_available = True
        self.rating = rating

    def accept_delivery(self):
        if self.is_available:
            self.is_available = False
            return True
        return False

    def update_location(self, location):
        self.location = location

    def mark_delivered(self):
        self.is_available = True


# -------------------- Order --------------------
class Order:
    def __init__(self, order_id, customer_id, restaurant_id, items):
        self.order_id = order_id
        self.customer_id = customer_id
        self.restaurant_id = restaurant_id
        self.items = items
        self.status = "Created"
        self.total_amount = 0

    def place(self, restaurant, cart_total):
        if not restaurant.accept_order():
            print("Restaurant rejected order")
            self.status = "Rejected"
            return

        self.total_amount = cart_total
        self.status = "Placed"
        print("Order placed successfully")

    def cancel(self):
        self.status = "Cancelled"
        print("Order cancelled")

    def update_status(self, status):
        self.status = status

    def get_eta(self):
        return sum(item.preparation_time for item in self.items)


# -------------------- Rating --------------------
class Rating:
    def __init__(self, order_id, restaurant_rating, delivery_rating, review):
        self.rating = (restaurant_rating + delivery_rating) / 2
        self.order_id = order_id
        self.restaurant_rating = restaurant_rating
        self.delivery_rating = delivery_rating
        self.review = review

    def validate(self):
        return 1 <= self.restaurant_rating <= 5 and 1 <= self.delivery_rating <= 5

    def submit(self):
        if self.validate():
            print("Rating submitted")
        else:
            print("Invalid rating")


# -------------------- MAIN EXECUTION --------------------

# Create restaurant
r = Restaurant(1, "A2B", "South Indian", rating=4.2)

# Create menu items
item1 = MenuItem(1, "Idli", 50, "Food", True, 5)
item2 = MenuItem(2, "Dosa", 80, "Food", True, 10)

# Add items to restaurant
r.add_menu_item(item1)
r.add_menu_item(item2)

# Create cart
cart = Cart(1, 101)
cart.add_item(item1)
cart.add_item(item2)

# Add more items (extra example)
item4 = MenuItem(4, "Vada", 30, "Snack", True, 5)
item5 = MenuItem(5, "Coffee", 20, "Drink", True, 3)

r.add_menu_item(item4)
r.add_menu_item(item5)

cart.add_item(item4)
cart.add_item(item5)

# Apply promo
cart.apply_promo("DISCOUNT10")

# Checkout
cart_total = cart.checkout()
print("Cart Total:", cart_total)

# Create order
order = Order(201, 101, r.restaurant_id, cart.items)
order.place(r, cart_total)

print("ETA:", order.get_eta(), "minutes")

# Delivery Partner
partner = DeliveryPartner(1, "Ravi", "9876543210", "Chennai", 4.5)

if partner.accept_delivery():
    print("Partner assigned:", partner.name)

partner.update_location("Near customer")
partner.mark_delivered()

order.update_status("Delivered")
print("Order Status:", order.status)

# Rating
rating = Rating(order.order_id, 5, 4, "Good service")
rating.submit()