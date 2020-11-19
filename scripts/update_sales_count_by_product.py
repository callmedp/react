# Python core imports
import time
import functools
import logging
from collections import Counter

# Django Core Imports
from django.db import connection, reset_queries

# Inter App Imports
from order.models import OrderItem
from shop.models import Product


def query_debugger(func):
    """
    Decorator to measure the execution time and the
    the number of queries executed
    by in the function
    """

    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        reset_queries()

        start_queries = len(connection.queries)

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        end_queries = len(connection.queries)

        print(f"Function : {func.__name__}")
        print(f"Number of Queries : {end_queries - start_queries}")
        print(f"Finished in : {(end - start):.2f}s")
        return result

    return inner_func


@query_debugger
def update_sales_count_product():
    command = "update_sales_by_product"
    if __name__ == '__main__':

        try:
            queryset = OrderItem.objects.select_related('order') \
                .filter(order__status__in=[1, 2, 3, 4]) \
                .values_list('product', flat=True)

            product_query_list = list(Product.objects.all())

            by_id_product_counts = Counter(queryset)

            for product in product_query_list:
                product.buy_count = by_id_product_counts[product.id]

            Product.objects.bulk_update(product_query_list, ['buy_count'])

            logging.getLogger('info_log').info(
                'Found total {} Order Item and Updated {} Products'.format(queryset.count(),
                                                                           by_id_product_counts.__len__()))

        except Exception as e:
            logging.getLogger('error_log').info(
                'Error occurred while update Sales count on Product. Debug Info {}'.format(str(e)))


if __name__ == '__main__':
    update_sales_count_product()
