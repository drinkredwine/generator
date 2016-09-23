import json
import random
import uuid

import requests
import time

r = requests.get('https://randomuser.me/api/', data = { 'dataType': 'json' })

CR_VIEW_BASKET = 0.2
CR_BASKET_PURCHASE = 0.33

BROWSER = ['Chrome', 'Safari', 'Firefox', 'Opera', 'IE', 'Other']
OS = ['Windows', 'Mac OSX', 'iOS', 'Android', 'Linux', 'Other']
DEVICE = ['Desktop', 'Tablet', 'Mobile']
UTM_CAMPAIGN = ['FB_ads1', 'FB_ads2', 'FB_ads3', 'Newsletter_1', 'Newsletter_2','Newsletter_3', 'CrossPromo_1',
                'Promo 2', 'invite', 'social share', 'affiliate 1', 'affiliate 2', 'affiliate 3']
UTM_SOURCE = ['PPC', 'social', 'blog', 'affiliate']
SEARCH = ['stabile', 'Stabile', 'Adidas', 'Adi', 'Ad', 'XL', 'L', 'XXL','XS', 'Puma', 'coffe maker', 'discout']
CATEGORY = ['Shoes', 'Women appeal', 'Men appeal', 'Accessories', 'Other']
PRODUCTS = [
    {'name': 'Stabile 3', 'brand': 'Adidas', 'category': 'Shoes', 'price': 60, 'discount':0},
    {'name': 'Stabile 5', 'brand': 'Adidas', 'category': 'Shoes', 'price': 70, 'discount': 0},
    {'name': 'Stabile 5', 'brand': 'Puma', 'category': 'Shoes', 'price': 50, 'discount': 0},
    {'name': 'Skirt A-shaped', 'brand': 'Hand made', 'category': 'Women apparel', 'price': 90, 'discount': 0},
    {'name': 'Skirt A-shaped', 'brand': 'Hand made', 'category': 'Women apparel', 'price': 90, 'discount': 0},
    {'name': 'T-shirt XXL', 'brand': 'Nike', 'category': 'Men apparel', 'price': 19.90, 'discount': 0},
    {'name': 'T-shirt XL', 'brand': 'Nike', 'category': 'Men apparel', 'price': 19.90, 'discount': 10},
    {'name': 'T-shirt L', 'brand': 'Nike', 'category': 'Men apparel', 'price': 19.90, 'discount': 5},
    {'name': 'T-shirt M', 'brand': 'Nike', 'category': 'Men apparel', 'price': 19.90, 'discount': 0},
    {'name': 'T-shirt S', 'brand': 'Nike', 'category': 'Men apparel', 'price': 19.90, 'discount': 0},
    {'name': 'T-shirt XXL', 'brand': 'Puma', 'category': 'Women apparel', 'price': 29.90, 'discount': 0},
    {'name': 'T-shirt XL', 'brand': 'Puma', 'category': 'Women apparel', 'price': 29.90, 'discount': 10},
    {'name': 'T-shirt L', 'brand': 'Puma', 'category': 'Women apparel', 'price': 29.90, 'discount': 0},
    {'name': 'T-shirt M', 'brand': 'Puma', 'category': 'Women apparel', 'price': 29.90, 'discount': 0},
    {'name': 'T-shirt S', 'brand': 'Puma', 'category': 'Women apparel', 'price': 29.90, 'discount': 0}
]
DELIVERY = ['courier','mail','personally', 'digital']
PAYMENT = ['Credit card', 'Paypal', 'Loyalty points']


class Generator(object):
    def __init__(self, user_count):
        self.users_count = user_count
        self.users = []

        return

    def print(self):
        print(self.users)
        for user in self.users:
            print(user['events'])

    def _save(self, data, file):
        with open(file, mode="w+", encoding="utf-8") as f:
            f.write(" ".join(data[0].keys()))
            for item1 in data:
                item = item1
                item.pop('cart', None)
                item.pop('events', None)

                out = ' '.join(map(str, item.values()))
                f.write(out+"\n")

    def save(self):
        users = self.users
        self._save(users, 'customers.csv')
        files = {}
        for user in users:
            for event in user['events']:
                props = event['properties']
                event = event.update(props)
                event.pop('properties', None)

                row = ' '.join(map(str, event.values()))

                if event['type'] not in files:
                    files[event['type']]=[]

                files[event['type']].append(row+"\n")

        for event_type, rows in files.items():
            with open(event_type+".csv", "w+", newline="\n") as f:
                f.write(' '.join(map(str, rows.values())))
                print(rows)
                f.writelines(rows)
        return

    def _save(self, data, file):
        with open(file, mode="w+", encoding="utf-8") as f:
            user = data[0]
            user.pop('cart', None)
            user.pop('events', None)
            f.write(" ".join(map(str, data[0].keys())))

            for item in data:
                item.pop('cart', None)
                item.pop('events', None)
                out = ' '.join(map(str, item.values()))
                f.write(out)
        return

    def generate(self):
        self.generate_users()
        self.generate_events()
        with open('data.json', mode='w+', encoding='utf-8') as f:
            f.write(json.dumps(self.users))

    def generate_users(self):
        users = requests.get('https://randomuser.me/api/?results='+str(self.users_count), data={'dataType': 'json', })

        for i, user in enumerate(users.json()['results']):
            print(user)
            created_ts = time.time() + random.randint(1,3600*24*14) - random.randint(1,3600*24*90)
            data = {
                'registered': i,
                'cookie_id': str(uuid.uuid4()),
                'first name': user['name']['first'],
                'last name': user['name']['last'],
                'email': user['email'],
                'city': user['location']['city'],
                'image': user['picture']['thumbnail'],
                'gender': user['gender'],
                'created_ts': created_ts,
                'last_activity_ts': created_ts,
                'events': [],
                'cart': []
            }

            self.users.append(data)

        return

    def generate_events(self):
        for user in self.users:
            self.generate_user_journey(user)

    def generate_user_journey(self, user):
        timestamp = user['created_ts']
        for i in range(0, random.randint(0,20)):
            self.generate_session(user, timestamp)
            user['last_activity_ts'] += random.randint(3600*4*1, 3600*30*24)
            if user['last_activity_ts'] >= time.time()+3600*24*30:
                break

        return

    def generate_session(self, user, timestamp):

        self.generate_visit(user, timestamp, "start")
        [self.generate_browse(user, timestamp, max_cycles=3) for i in range(0, random.randint(0, 5))]
        self.generate_visit(user, timestamp, "end")
        return

    def generate_browse(self, user, timestamp, max_cycles):
        for loop in range(0,random.randint(0,max_cycles)):
            [self.generate_find(user) for i in range(0, random.randint(0, 3))]
            [self.generate_view(user) for i in range(0, random.randint(0, 5))]

        return timestamp

    def _get_value(self, items, chance):
        for item in items:
            if random.random()<=chance:
                return item
        return items[-1]

    def generate_visit(self, user, timestamp, stage="start"):
            if stage == 'end':
                user['last_activity_ts'] += random.randint(30, 0.5 * 3600)
            properties = {
                'browser': self._get_value(BROWSER, 0.45),
                'os': self._get_value(OS, 0.3),
                'device': self._get_value(DEVICE, 0.4),
                'utm_campaign': self._get_value(UTM_CAMPAIGN, 0.1),
                'utm_source': self._get_value(UTM_SOURCE, 0.2)
            }
            event = {
                'timestamp': user['last_activity_ts'],
                'type': 'session_'+stage,
                'customer_id': user['registered'],
                'properties': properties
            }
            if stage == 'end':
                event['duration'] = random.randint(10, 9000)

            user['events'].append(event)
            return

    def generate_find(self, user):
        user['last_activity_ts'] += random.randint(30, 0.5*3600)
        properties = {
            'search': self._get_value(SEARCH, 0.1),
            'category': self._get_value(CATEGORY, 0.2),
        }
        event = {
            'timestamp': user['last_activity_ts'],
            'type': 'find',
            'customer_id': user['registered'],
            'properties': properties
        }

        user['events'].append(event)

        return

    def generate_view(self, user):
        user['last_activity_ts'] += random.randint(30, 0.5*3600)
        properties = self._get_value(PRODUCTS, 0.08)
        event = {
            'timestamp': user['last_activity_ts'],
            'type': 'view',
            'customer_id': user['registered'],
            'properties': properties
        }
        user['events'].append(event)
        if(random.random() <= CR_VIEW_BASKET):
            self.generate_add_to_basket(user, properties)

        return

    def generate_add_to_basket(self, user, item):
        user['last_activity_ts'] += random.randint(30, 0.5*3600)
        user['cart'].append(item)
        properties = item
        event = {
            'timestamp': user['last_activity_ts'],
            'type': 'add to basket',
            'customer_id': user['registered'],
            'properties': properties
        }
        user['events'].append(event)

        if(random.random() <= CR_BASKET_PURCHASE):
            self.generate_purchase(user)
        return

    def generate_purchase(self, user):
        user['last_activity_ts'] += random.randint(30, 0.5*3600)
        total_price = 0
        items = 0
        for item in user['cart']:
            total_price += item['price']
            items += 1

        properties = {
            'total price':total_price,
            'items': items,
            'delivery method': self._get_value(DELIVERY, 0.6),
            'payment method': self._get_value(PAYMENT, 0.5)
        }
        event = {
            'timestamp': user['last_activity_ts'],
            'type': 'purchase',
            'customer_id': user['registered'],
            'properties': properties
        }
        user['events'].append(event)
        user['cart'] = []
        return







