import json
import random
import time
import uuid
from copy import copy
from os import path

import requests

CR_VIEW_BASKET = 0.003
CR_BASKET_PURCHASE = 0.07

BROWSER = ['Chrome', 'Safari', 'Firefox', 'Opera', 'IE', 'Other']
OS = ['Windows', 'Mac OSX', 'iOS', 'Android', 'Linux', 'Other']
DEVICE = ['Desktop', 'Tablet', 'Mobile']
UTM_CAMPAIGN = ['FB_ads1', 'FB_ads2', 'FB_ads3', 'Newsletter_1', 'Newsletter_2','Newsletter_3', 'CrossPromo_1',
                'Promo 2', 'invite', 'social share', 'affiliate 1', 'affiliate 2', 'affiliate 3']
UTM_SOURCE = ['FB-PPC', 'Google-PPC', 'social', 'blog', 'affiliate']
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
        self.now = time.time()

        return

    def print(self):
        print(self.users)
        for user in self.users:
            print(user['events'])

    def save(self):
        self._save_customers(self.users, 'data/customers.csv')
        self._save_events()
        return

    def track(self):
        self._track_users()
        self._track_events()
        return

    def _track_users(self):
        commands = []
        for i, user in enumerate(self.users):
            cmd = {
                'name': 'crm/customers',
                'data': {
                    'customer_ids': {
                        'registered': user['registered_id']
                    },
                    'project_id': 'e1d184f2-843b-11e6-b121-141877340e97'
                }
            }
            cmd['data'].update({k: v for k, v in user.items() if k not in ['events','cart','last_activity_ts']})

            commands.append(cmd)
            if i % 1000:
                self._call_exponea_bulk_api(commands)
                commands = []

            self._call_exponea_bulk_api(commands)

    def _track_events(self):
        commands = []
        counter = 0
        for i, user in enumerate(self.users):
            for j, event in enumerate(user['events']):
                counter += 1
                cmd = {
                    'name': 'crm/events',
                    'data': {
                        'customer_ids': {
                            'registered': user['registered_id']
                        },
                     'project_id': 'e1d184f2-843b-11e6-b121-141877340e97'
                    }
                }
                cmd['data'].update({k: v for k, v in event.items() if k not in ['registered_id']})

                commands.append(cmd)
                if counter % 1000:
                    self._call_exponea_bulk_api(commands)
                    commands = []

            self._call_exponea_bulk_api(commands)

    @staticmethod
    def _call_exponea_bulk_api(self, commands):
        try:
            r = requests.post("https://api.exponea.com/bulk", #data=json.dumps(commands),
                              json={'commands': commands},
                              headers={'content-type': "application/json"})
        except Exception as e:
            print(e)

    def _save_events(self):
        files = {}

        for user in self.users:
            for event in user['events']:
                row = str()
                if event['type'] not in files:
                    files[event['type']] = []
                    event_atoms = {k: v for k, v in event.items() if k != 'properties'}
                    row += ';'.join(map(str, list(event_atoms.keys()) + list(event['properties'].keys()) ))+'\n'

                event_atoms = {k: v for k, v in event.items() if k != 'properties'}
                row += ';'.join(map(str, list(event_atoms.values()) + list(event['properties'].values()) ))+'\n'

                files[event['type']].append(row)

        for event_type, rows in files.items():
            with open(path.join("data", event_type + ".csv"), "w+", newline="\n") as f:
                f.write(''.join(map(str, rows)))
        return

    def _save_customers(self, data, file):
        with open(file, mode="w+", encoding="utf-8", newline="\n") as f:
            user = copy(data[0])
            user.pop('cart', None)
            user.pop('events', None)
            f.write(';'.join(map(str, user.keys())))

            for item_instance in data[1:]:
                item = copy(item_instance)
                item.pop('cart', None)
                item.pop('events', None)
                out = '\n'+(';'.join(map(str, item.values())))
                f.write(out)
        return

    def generate(self):
        self.generate_users()
        self.generate_events()
        with open('data.json', mode='w+', encoding='utf-8') as f:
            f.write(json.dumps(self.users))
        return

    def get_users_from_api(self):
        query = 'https://randomuser.me/api'
        payload = {'results': self.users_count}
        r = requests.get(query, params=payload)
        users = r.json()['results']
        return users

    def get_users_from_file(self):
        with open('users_10k.json','r') as f:
            users = json.load(f)
        return users

    def generate_users(self):

        users = self.get_users_from_api()
#        users = self.get_users_from_file()

        print(len(users))
        for i, user in enumerate(users):
            created_ts = time.time() + random.randint(1,3600*24*14) - random.randint(1,3600*24*90)

            data = {
                'registered_id': i,
                'cookie_id': str(uuid.uuid4()),
                'first name': user['name']['first'],
                'last name': user['name']['last'],
                'email': user['email'],
                'city': user['location']['city'],
                'image': user['picture']['medium'],
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
        # 25% empty session
        if float(user['registered_id'] % 3) == 0:
            return timestamp

        for loop in range(0,random.randint(0,max_cycles)):
            [self.generate_find(user) for i in range(0, random.randint(0, 3))]
            [self.generate_view(user) for i in range(0, random.randint(0, 5))]

        return timestamp

    def _get_value(self, items, chance):
        for item in items:
            if random.random() <= chance:
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
                'timestamp': user['last_activity_ts'] - self.now,
                'type': 'session_'+stage,
                'registered_id': user['registered_id'],
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
            'timestamp': user['last_activity_ts'] - self.now,
            'type': 'find',
            'registered_id': user['registered_id'],
            'properties': properties
        }

        user['events'].append(event)

        return

    def generate_view(self, user):
        user['last_activity_ts'] += random.randint(30, 0.5*3600)
        properties = self._get_value(PRODUCTS, 0.08)
        event = {
            'timestamp': user['last_activity_ts'] - self.now,
            'type': 'visit_item',
            'registered_id': user['registered_id'],
            'properties': properties
        }
        user['events'].append(event)
        if random.random() <= CR_VIEW_BASKET * float(user['registered_id'] % 9):

            if user['events'][0]['properties'].get('utm_source',"") == 'FB-PPC' and random.random() > 0.10:
                return
            else:
                self.generate_add_to_cart(user, properties)

        return

    def generate_add_to_cart(self, user, item):
        user['last_activity_ts'] += random.randint(30, 0.5*3600)
        user['cart'].append(item)
        properties = item
        event = {
            'timestamp': user['last_activity_ts'] - self.now,
            'type': 'add_to_cart',
            'registered_id': user['registered_id'],
            'properties': properties
        }
        user['events'].append(event)

        if random.random() <= CR_BASKET_PURCHASE * (user['registered_id'] % 10):
            self.generate_purchase(user)
        return

    def generate_purchase(self, user):
        user['last_activity_ts'] += random.randint(30, 0.5*3600)
        total_price = 0
        items = 0

        for item in user['cart']:
            total_price += item['price']
            self.generate_purchase_item(user, item)
            items += 1

        properties = {
            'total price':total_price,
            'items': items,
            'delivery method': self._get_value(DELIVERY, 0.6),
            'payment method': self._get_value(PAYMENT, 0.5)
        }

        event = {
            'timestamp': user['last_activity_ts'] - self.now,
            'type': 'purchase',
            'registered_id': user['registered_id'],
            'properties': properties
        }

        user['events'].append(event)
        user['cart'] = []
        return

    def generate_purchase_item(self, user, item):
        properties = {
            'price': item['price'],
            'quantity': 1
        }

        event = {
            'timestamp': user['last_activity_ts'] - self.now,
            'type': 'purchase_item',
            'registered_id': user['registered_id'],
            'properties': properties
        }
        user['events'].append(event)

        return






