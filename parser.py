import json
from dataclasses import dataclass

import requests

@dataclass(frozen=True)
class Product():
    name : any = ''
    restaurant : any = ''
    energy_value : float = 0
    fat : float = 0
    prot : float = 0
    carbs : float = 0
    mass : float = 0
    price : float = 0


class IRestaurantParser():
    def get_products(self) -> Product:
        raise NotImplementedError()

    def __repr__(self):
        raise NotImplementedError()


class KFCParser(IRestaurantParser):
    def __get_menu(self):
        products_url = 'https://app-api.kfc.ru/cache/en/api/v1/common/product/master-menu'
        server_response = requests.get(products_url)
        products = json.loads(server_response.text)
        return products

    def __validate_value(self, value):
        return value if value is not None else 0
    
    def get_products(self):
        product_list_json = self.__get_menu()
        product_list = []
        for product in product_list_json['data']:
            name = product['title']
            restaurant = 'KFC'
            energy_value = self.__validate_value(product['energy_value'])
            fat = self.__validate_value(product['fat'])
            prot = self.__validate_value(product['protein'])
            carbs = self.__validate_value(product['starch'])
            mass = self.__validate_value(product['mass'])
            price = self.__validate_value(product['price'])

            product = Product(
                name=name, restaurant=restaurant,
                energy_value=energy_value,
                fat=fat, prot=prot,
                carbs=carbs, mass=mass,
                price=price)            
            
            product_list.append(product)
        return product_list

    def __str__(self):
        return 'KFC'

    def __repr__(self):
        return 'KFC'


class BurgerKingParser(IRestaurantParser):
    def __get_menu(self):
        products_url = 'https://orderapp.burgerking.ru/api/v1/menu/?restaurant=363'
        server_response = requests.get(products_url)
        products = json.loads(server_response.text)
        return products

    def __validate_value(self, value):
        return value if value is not None else 0

    def get_products(self):
        product_list = []
        product = self.__get_menu()
        for category in product['response']['categories']:
            for dish in category['dishes']:
                nutritional_values = dish['info']['composition']
                name = dish['name']
                restaurant = 'Burger King'
                energy_value = self.__validate_value(nutritional_values['kcal_100'])
                fat = self.__validate_value(nutritional_values['fats_100'])
                prot = self.__validate_value(nutritional_values['protein_100'])
                carbs = self.__validate_value(nutritional_values['carbs_100'])
                mass = self.__validate_value(nutritional_values['weight'])
                price = (self.__validate_value(dish['price'])/100)

                product = Product(
                    name=name, restaurant=restaurant,
                    energy_value=energy_value,
                    fat=fat, prot=prot,
                    carbs=carbs, mass=mass,
                    price=price)

                product_list.append(product)
        return product_list

    def __repr__(self):
        return 'Burger King'


class McdonaldsParser(IRestaurantParser):
    def _get_json(self, url):
        return json.loads(requests.get(url).text)

    def _get_categories(self):
        categories_url = 'https://mcdonalds.ru/api/menu'
        categories_list = []
        categories_json = self._get_json(categories_url)
        for category in categories_json['categories']:
            categories_list.append(category['alias'])
        return categories_list

    def get_products(self):
        category_url = 'https://mcdonalds.ru/api/menu/category/{category_name}'
        product_list = []
        categories = self._get_categories()
        for category in categories:
            category = self._get_json(category_url.format(category_name=category))
            for product in category['products']:
                nutritional_values = product['offers'][0]['nutritionalValue']
                if (nutritional_values != None):
                    name = product['name']
                    restaurant = 'McDonalds'
                    energy_value = nutritional_values['energyCal']['amount'].replace(',', '.')
                    fat = nutritional_values['fat']['amount'].replace(',', '.')
                    prot = nutritional_values['protein']['amount'].replace(',', '.')
                    carbs = nutritional_values['carbohydrate']['amount'].replace(',', '.')
                    #mass = None
                    price = product['offers'][0]['price']
                    try:
                        product = Product(name=name, restaurant=restaurant,
                        energy_value=float(energy_value), fat=float(fat),
                        prot=float(prot), carbs=float(carbs),
                        price=float(price))

                        product_list.append(product)
                    except(ValueError):
                        print("Значение полученное с сервера говно")
                        
        return product_list

    def __str__(self):
        return 'McDonalds'

    def __repr__(self):
        return 'McDonalds'


class ParserController():
    def __init__(self):
        self.__restaurants_parsers = []

    def add_parser(self, restaurant_parser):
        if isinstance(restaurant_parser, IRestaurantParser): 
            self.__restaurants_parsers.append(restaurant_parser)
        else:
            raise TypeError('Парсер должен быть наследником IRestaurantParser')
    
    def get_restaurants(self):
        return self.__restaurants_parsers
    
    #Предлагаю реализовать фильтр на стороне клинета, будет удобнее.
    def get_products(self, max_prot=9999, max_price=9999, max_kcal=9999, max_fat=9999):
        cached_products = []
        for parser in self.__restaurants_parsers:
            cached_products.extend(parser.get_products())

        cache_size = len(cached_products)
        index = 0
        while (index < cache_size):
            if cached_products[index].prot > max_prot: 
                del cached_products[index]
            elif cached_products[index].price > max_price: 
                del cached_products[index]
            elif cached_products[index].energy_value > max_kcal: 
                del cached_products[index]
            elif cached_products[index].fat > max_fat: 
                del cached_products[index]
            else: 
                cache_size = cache_size + 1
                index = index + 1
            cache_size = cache_size - 1
        return cached_products
