import parser
import utils

rest_parser = parser.ParserController()

#Добавляю встроеные парсеры(можно написать свой парсер, если он унаследован от IRestaurantParser)
rest_parser.add_parser(parser.KFCParser())
rest_parser.add_parser(parser.BurgerKingParser())
rest_parser.add_parser(parser.McdonaldsParser())

products = rest_parser.get_products()
max_price = float(input('Введите бюджет: '))

#Здесь я конвертирую свою структуры данных в твою, для поддержания корректной работы функции
"""
ISSUE:
Твоя функция не переваривет float(только int)
"""
corr_prod = [utils.Product(p.name, int(p.price), int(p.energy_value)) for p in products]

best_combo = utils.maximize_kcal(corr_prod, max_price)

print(rest_parser.get_restaurants())

