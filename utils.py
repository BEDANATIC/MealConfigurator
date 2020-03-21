from collections import namedtuple
from operator import attrgetter
Product = namedtuple('Product', 'name price kcal')


class ProductSet:
    """Вспомошательный класс, экземпляр которого возвращается функцией maximize_kcal"""
    def __init__(self, indexes, kcal):
        self.indexes, self.kcal = indexes, kcal

    def __add__(self, other):
        return ProductSet(self.indexes | other.indexes, self.kcal + other.kcal)


def maximize_kcal(products, cost_limit, cost_step=5):
    """
    maximize_kcal(products, cost_limit, cost_step=5)
    Ищет набор продуктов с наибольшим количеством килокалорий, укладывающийся в данный бюджет.

    Аргументы:
    products -- список продуктов. Продукт здесь -- это экземпляр класса, имеющий, как минимум,
    атрибуты name, price, kcal.
    cost_limit -- доступный бюджет.
    cost_step -- шаг алгоритма. Рекомендуется выставлять по наименьшему общему кратному цен всех продуктов.
    По умолчанию равен 5.

    Возвращает экземпляр класса ProductSet с двумя атрибутами:
    indexes -- индексы продуктов из входного списка.
    kcal -- общая калорийность.

    """
    cost_limit = (cost_limit // cost_step) * cost_step
    cell = []
    for i in range(len(products)):
        cell.append([])
        for j in range(cost_limit // cost_step):
            cost = (j + 1) * cost_step
            var1 = cell[i-1][j] if i > 0 else ProductSet(set(), 0)
            if products[i].price < cost and i > 0:
                var1 = cell[i - 1][j]
                var2 = (ProductSet({i}, products[i].kcal) +
                        cell[i - 1][(cost - products[i].price) // cost_step - 1])
            elif products[i].price <= cost:
                var2 = ProductSet({i}, products[i].kcal)
            else:
                var2 = ProductSet(set(), 0)
            cell[i].append(max(var1, var2, key=attrgetter('kcal')))
    return cell[len(products) - 1][cost_limit // cost_step - 1]


products = [Product('Картошка фри', 15, 50),
            Product('Двойной гамбургер', 30, 200),
            Product('Куриные крылья', 20, 150),
            ]

answer = maximize_kcal(products, 65)
print(', '.join([products[i].name for i in answer.indexes]))
print(answer.kcal, 'ккал')
 
