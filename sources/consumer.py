"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time: int = retry_wait_time
        Thread.__init__(self, **kwargs)

    def print_carts(self, id_cart):
        """
        Prints the products in the cart

        type id_cart: int
        :param id_cart: cart id
        """

        #obtin lista de produse din market place, iar apoi apelez functia de printare
        list_order = self.marketplace.place_order(id_cart)
        for product in list_order:
            self.marketplace.print_cons(self.name, product)


    def add_product_to_cart(self, id_cart, prod):
        """
        type id_cart: int
        :param id_cart: cart id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

            prints the products in the cart
        """
        #scoate produsul din marketplace, daca primeste false, asteapta si reincearca
        go_next = self.marketplace.add_to_cart(id_cart,prod)
        if go_next is False:
            time.sleep(self.retry_wait_time)
            self.add_product_to_cart(id_cart, prod)


    def run(self):
        id_cart = self.marketplace.new_cart()
        for products in self.carts:
            for produs in products:
                for _ in range(produs["quantity"]):
                    if produs["type"] == "remove":
                        self.marketplace.remove_from_cart(id_cart, produs)
                    else:
                        self.add_product_to_cart(id_cart, produs)
        self.print_carts(id_cart)
