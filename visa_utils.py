class Category:
    fun = 'fun'
    clothes = "clothes"
    dog = "dog"
    amazon = "amazon"
    none = "-"
    groceries = "groceries"
    muffin = "muffin"
    interest = "interest"
    meds = "meds"
    flight = "flight"
    unsure = "unsure"
    restaurant = "restaurant"
    weed = "weed"
    gift = "gift"
    phone = "phone"
    snacks = "snacks"
    transit = "transit"
    subscription = "subscription"
    parking = 'parking'


class Item:
    def __init__(self, store, need='no', category=Category.none):
        self.store = store
        self.need = need
        self.category = category


def print_section(message, start=True):
    if start:
        print(f'----- {message} - start -----')
    else:
        print(f'----- {message} - end -----')
