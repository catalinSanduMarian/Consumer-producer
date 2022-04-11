"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
from threading import Lock
import logging
from logging.handlers import RotatingFileHandler
import time

#intializing the logger
logger = logging.getLogger('loggerOne')
logger.setLevel(logging.INFO)

#10 filies of ~500KB
handler = RotatingFileHandler('file.log', maxBytes=500000, backupCount=10)

#THE forma it : "time(GMT) Logging level: message"
formatter = logging.Formatter('%(asctime)s %(levelname)8s: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

#converting to gmt
logging.Formatter.converter = time.gmtime


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """

    def __init__(self, queue_size_per_producer):
        """
        Constructor
        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        #multe variabile de care ma folosesc in functii 

        logger.info("init Marketplace, argument qsise: %d", queue_size_per_producer)
        self.queue_size_per_producer = queue_size_per_producer
        self.id_prod = 0
        self.id_cart = 0
        self.producers = []
        self.producers.append(0)
        self.products = []
        self.products.append([])
        self.carts = []
        #toate lockurile
        self.add_to_cart_lock = Lock()
        self.publish_lock = Lock()
        self.print_lock = Lock()
        self.new_cart_lock = Lock()
        self.register_producer_lock = Lock()
        self.remove_from_cart_lock = Lock()

        logger.info("init Marketplace, all")

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        #lock pt ca id prod/printurile pot face race condition
        self.register_producer_lock.acquire()
        logger.info("register_producer, id_prod =%d", self.id_prod)
        self.producers.append(self.queue_size_per_producer)
        self.id_prod = self.id_prod + 1
        self.products.append([])
        self.register_producer_lock.release()

        logger.info("register_producer, id_prod-exit =%d", self.id_prod)
        return self.id_prod

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        #daca produce, returneaza adev, altfel fals
        it_produced = False
        #lock pt ca printatul si adaugatul in lista pot da race condition
        self.publish_lock.acquire()
        logger.info("publish; id_producer =%d", producer_id)
        if self.producers[producer_id] > 0:
            self.products[producer_id].append(product[0])
            self.producers[producer_id] = self.producers[producer_id] -1
            it_produced = True

        logger.info("publish; exit =%d", producer_id, )
        self.publish_lock.release()
        return it_produced


    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        #lock pt ca printatul si op pe id_cart pot da race condition

        self.new_cart_lock.acquire()
        logger.info("new_cart;")

        self.carts.append([])
        current_cart_id = self.id_cart
        self.id_cart = self.id_cart+1

        logger.info("new_cart; iese")
        self.new_cart_lock.release()

        return current_cart_id


    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        #daca nu gasesc produsul returnez fals
        producer_found_id = 0
        product_found = False
        available_product = []

        #lock pt ca printatul si adaugatul in lista pot da race condition
        #de asemenea, daca caut in lista si produsul este scos, am race condtion 
        self.add_to_cart_lock.acquire()
        logger.info("ad_to_cart %d;", cart_id)

        for producer in self.products:
            for available_product in producer:
                if product["product"] == available_product:
                    product_found = True
                    break

            if product_found:
                break
            producer_found_id = producer_found_id + 1

        if product_found:
            self.products[producer_found_id].remove(available_product)
            self.producers[producer_found_id] = self.producers[producer_found_id] + 1
            self.carts[cart_id].append(available_product)
            logger.info("ad_to_cart exit True;")
            self.add_to_cart_lock.release()
            return True

        logger.info("ad_to_cart exit False;")
        self.add_to_cart_lock.release()
        return False


    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """

        product_found = False
        producer_found_id = 0
        available_product = []

        #lock pt ca printatul si adaugatul in lista pot da race condition
        # daca gasesc un produs si e deja scos, am race condition
        self.remove_from_cart_lock.acquire()
        logger.info("reomce_from_cart start True;%d", cart_id)
        for available_product in self.carts[cart_id]:
            if product["product"] == available_product:
                product_found = True
                break
            producer_found_id = producer_found_id + 1

        if product_found:
            del self.carts[cart_id][producer_found_id]
            self.products[0].append(available_product)

        logger.info("ad_to_cart exit;")
        self.remove_from_cart_lock.release()


    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        #returnez lista de produse si golesc cartul
        logger.info("place_order start %d;", cart_id)
        copie =self.carts[cart_id]
        self.carts[cart_id] = []
        logger.info("place_order end;")
        return copie


    def print_cons(self, name, product):
        """
        Prints the product and name

        :type name: String
        :param name: cart name

        :type product: Product
        :param product: the product to print
        """
        #lock pt ca printatul poate da race condition
        self.print_lock.acquire()
        logger.info("print_cons start; name=%s;", name)
        print(name, "bought", product)
        self.print_lock.release()
