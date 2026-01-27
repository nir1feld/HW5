# TODO add all imports needed here
import json

class InvalidIdException(Exception):
    pass


class InvalidPriceException(Exception):
    pass


def check_ids(message, *ids):
    for id in ids:
        if id < 0:
            raise InvalidIdException(message)


class Entity:
    def __init__(self, id, name, city, address):
        check_ids(f"{__name__} ID must be non negative", id)

        self.id = id
        self.name = name
        self.city = city
        self.address = address

    def __rpr__(self):
        class_name = type(self).__name__
        return f"{class_name}(id='{self.id}', name='{self.name}', city ='{self.city}, address={self.address})"


class Customer(Entity):
    """
    Represents a customer in the Matamazon system.

    Required fields (per specification):
        - id (int): Unique non-negative integer identifier.
        - name (str): Customer name.
        - city (str): Customer city.
        - address (str): Customer shipping address.

    Exceptions:
        InvalidIdException: If 'id' is not valid according to the specification.

    Printing:
        Must support printing in the following format (example):
            Customer(id=42, name='Daniel Elgarici', city='Karmiel, address='123 Main Street')
        Exact formatting requirements appear in the assignment PDF.
    """

    # TODO implement this class as instructed
    pass


class Supplier(Entity):
    """
    Represents a supplier in the Matamazon system.

    Required fields (per specification):
        - id (int): Unique non-negative integer identifier.
        - name (str): Supplier name.
        - city (str): Warehouse city (origin city for shipping).
        - address (str): Warehouse address.

    Exceptions:
        InvalidIdException: If 'id' is not valid according to the specification.

    Printing:
        Must support printing in the following format (example):
            Supplier(id=42, name='Yinon Goldshtein', city='Haifa, address='32 David Rose Street')
    """

    # TODO implement this class as instructed
    pass


class Product:
    """
    Represents a product sold on the Matamazon website.

    Required fields (per specification):
        - id (int): Unique non-negative integer identifier.
        - name (str): Product name.
        - price (float): Non-negative price.
        - supplier_id (int): ID of the supplier that provides the product.
        - quantity (int): Non-negative quantity in stock.

    Exceptions:
        InvalidIdException:
            - If id/supplier_id/quantity is invalid per specification.
        InvalidPriceException:
            - If price is invalid (e.g., negative).

    Printing:
        Must support printing in the following format (example):
            Product(id=101, name='Harry Potter Cushion', price=29.99, supplier_id=42, quantity=555)
    """

    def __init__(self, id, name, price, supplier_id, quantity):
        check_ids(f"{__name__} ID must be non negative", id, supplier_id)

        if price < 0:
            raise InvalidPriceException(f"{__name__} Price must be non negative")

        self.id = id
        self.name = name
        self.price = price
        self.supplier_id = supplier_id
        self.quantity = quantity

    # TODO implement this class as instructed

    def __rpr__(self):
        return f"Product(id='{self.id}', name='{self.name}', price ='{self.price}, supplier_id={self.supplier_id}, quantity={self.quantity})"

    def __lt__(self, other):
        return self.price < other.price


class Order:
    """
    Represents a placed order.

    Required fields (per specification):
        - id (int): Unique non-negative integer identifier (assigned by the system).
        - customer_id (int): ID of the customer who placed the order.
        - product_id (int): ID of the ordered product.
        - quantity (int): Ordered quantity (non-negative integer).
        - total_price (float): Total price for the order (non-negative).

    Exceptions:
        InvalidIdException:
            - If one of the ID fields is invalid.
        InvalidPriceException:
            - If total_price is invalid.

    Printing:
        Must support printing in the following format (example):
            Order(id=1, customer_id=42, product_id=101, quantity=10, total_price=299.9)

    """

    def __init__(self, id, customer_id, product_id, quantity, total_price):
        check_ids(f"{__name__} ID must be non negative", id, product_id)

        if total_price < 0:
            raise InvalidPriceException(f"{__name__} Price must be non negative")

        self.id = id
        self.customer_id = customer_id
        self.product_id = product_id
        self.quantity = quantity
        self.total_price = total_price

    # TODO implement this class as instructed
    def __repr__(self):
        return f"Order(id={self.id}, customer_id={self.customer_id}, product_id={self.product_id}, quantity={self.quantity}, total_price={self.total_price})"


class MatamazonSystem:
    """
    Main system class that stores and manages customers, suppliers, products and orders.

    The system must support:
        - Registering customers/suppliers (with unique IDs across both types).
        - Adding/updating products (must validate supplier existence).
        - Placing orders (validate product existence and stock).
        - Removing objects by ID and type (with dependency constraints).
        - Searching products by name/query and optional max price.
        - Exporting system state to a text file (customers/suppliers/products only).
        - Exporting orders to JSON grouped by supplier origin city.

    Notes:
        - The specification does not require specific internal fields. Any data structures are allowed,
          as long as the behaviors match the spec.
        - A parameterless constructor is required.
    """

    def __init__(self):
        """
        Initialize an empty Matamazon system.

        Requirements:
            - Must be parameterless.
            - Internal collections may be chosen freely (dict/list, etc.).
        """
        # TODO implement this method if needed
        self.customers = {}  # dictionary(id,costumer)
        self.suppliers = {}  # dictionary(id,supplier)
        self.products = {}  # dictionary(id,product)
        self.orders = {}  # dictionary(id,order)
        self.next_id = 1

    def register_entity(self, entity, is_customer):
        """
        Register a Customer or Supplier in the system.

        Args:
            entity: A Customer or Supplier object.
            is_customer (bool): True if entity is Customer, False if entity is Supplier.

        Raises:
            InvalidIdException:
                - If the entity ID is invalid.
                - If the entity ID already exists in the system (note: IDs must be unique across
                  customers AND suppliers).
        """
        # TODO implement this method as instructed
        check_ids(f"Customer id {entity.id} must be non negative", entity.id)

        if is_customer:
            if entity.id in self.customers:
                raise InvalidIdException(f"Customer id {entity.id} is already taken.")
            self.customers[entity.id] = entity
        else:
            if entity.id in self.suppliers:
                raise InvalidIdException(f"Supplier id {entity.id} is already taken.")
            self.suppliers[entity.id] = entity

    def add_or_update_product(self, product):
        """
        Add a new product or update an existing product.

        Behavior:
            - If product does not exist in system: add it.
            - If product exists:
                - It must belong to the same supplier as the existing one (same supplier_id),
                  otherwise raise InvalidIdException.
                - Update the stored product's fields according to the new product.

        Args:
            product: A Product object.

        Raises:
            InvalidIdException:
                - If the supplier_id does not exist in the system.
                - If attempting to update a product but supplier_id differs from the existing product.
        """
        # TODO implement this method as instructed
        if product.supplier_id not in self.suppliers:
            raise InvalidIdException(
                f"Product {product} is given with supplier id {product.supplier_id} that matches no supplier.")

        if product.id in self.products:
            old_product = self.products[product.id]
            if old_product.supplier_id != product.supplier_id:
                raise InvalidIdException(f"Product {product} is given with un matching supplier id")
            self.products[product.id] = product
        else:
            self.products[product.id] = product

    def place_order(self, customer_id, product_id, quantity=1):
        """
        Place an order for a product by a customer.

        Args:
            customer_id (int): Customer ID.
            product_id (int): Product ID.
            quantity (int, optional): Quantity to order. Defaults to 1.

        Returns:
            str: Status message according to specification:
                - "The order has been accepted in the system"
                - "The product does not exist in the system"
                - "The quantity requested for this product is greater than the quantity in stock"

        Behavior:
            - If product does not exist: return the relevant message.
            - If quantity requested > stock: return the relevant message.
            - Otherwise:
                - Decrease product stock by quantity.
                - Create a new Order with an auto-incremented system ID (starting at 1).
                - Store the order in the system.
                - Return success message.

        Notes:
            - The specification assumes quantity is an integer.
        """
        # TODO implement this method as instructed
        if product_id not in self.products:
            return "The product does not exist in the system"

        product = self.products[product_id]
        if quantity > product.quantity:
            return "The quantity requested for this product is greater than the quantity in stock."

        product.quantity -= quantity
        total_price = product.price * quantity
        order = Order(
            id=self.next_id,
            customer_id=customer_id,
            product_id=product_id,
            quantity=quantity,
            total_price=total_price
        )

        self.orders[order.id] = order
        self.next_id += 1
        return "The order has been accepted in the system"

    def remove_object(self, _id, class_type):

        """
        Remove an object from the system by ID and type.

        Args:
            _id (int): Object ID to remove.
            class_type (str): One of: "Customer", "Supplier", "Product", "Order"
                              (exact casing/spelling per assignment).

        Returns:
            int | None:
                - If removing an Order: return the ordered quantity of that order (to restore stock).
                - Otherwise: no return value required.

        Raises:
            InvalidIdException:
                - If _id is not a valid non-negative integer.
                - If attempting to remove a Customer/Supplier/Product that still has dependent orders
                  in the system (i.e., orders that were not removed).
                - Additional InvalidIdException conditions as required by specification.
        """
        # TODO implement this method as instructed
        check_ids(f"Remove object id {_id} must be non negative", id)
        class_type_clean = class_type.strip().lower()
        if class_type_clean == "order":
            if _id in self.orders:
                order = self.orders.pop(_id)
                if order.product_id in self.products:
                    self.products[order.product_id] += order.quantity
                return order.quantity
            return None

        elif class_type_clean == "customer":
            for order in self.orders.values():
                if order.customer_id == _id:
                    raise InvalidIdException("Cannot remove customer - still in use in existing orders")

            if _id in self.customers:
                self.customers.pop(_id)

        elif class_type_clean == "supplier":
            for order in self.orders.values():
                order_product = self.products[order.product_id]
                if order_product.supplier_id == _id:
                    raise InvalidIdException("Cannot remove supplier - still in use in existing orders")

            if _id in self.suppliers:
                self.suppliers.pop(_id)

        elif class_type_clean == "product":
            for order in self.orders.values():
                if order.product_id == _id:
                    raise InvalidIdException("Cannot remove product - still in use in existing orders")

            if _id in self.products:
                self.products.pop(_id)

        return None

    def search_products(self, query, max_price=None):
        """
        Search products by query in the product name, and optionally filter by max_price.

        Args:
            query (str): Product name or part of product name.
            max_price (float, optional): If provided, only return products with price <= max_price.

        Returns:
            list[Product]:
                - Products that match the query and have quantity != 0,
                - Sorted by ascending price.
                - If no matching products exist, return an empty list.
        """
        # TODO implement this method as instructed
        result = []
        for product in self.products.values():
            if product.quantity <= 0:
                continue

            if query in product.name:
                if max_price is None:
                    result.append(product)
                elif product.price <= max_price:
                    result.append(product)

        return sorted(result)

    def export_system_to_file(self, path):
        """
        Export system state (customers, suppliers, products) to a text file.

        Args:
            path (str): Output file path.

        Behavior:
            - Write each object on its own line, using the object's print/str representation.
            - Orders must NOT be included.
            - No constraint on the ordering of objects in the output.

        Raises:
            OSError (or any file-open exception): Must be propagated to the caller.
        """
        # TODO implement this method as instructed
        try:
            with open(path, 'w') as file:
                for customer in self.customers.values():
                    file.write(f"{customer}\n")

                for supplier in self.suppliers.values():
                    file.write(f"{supplier}\n")

                for product in self.products.values():
                    file.write(f"{product}\n")
        except Exception as e:
            raise e

    def export_orders(self, out_file):
        """
        Export orders in JSON format grouped by origin city.

        Args:
            out_file (file-like)

        Behavior (per specification):
            - Produce a JSON object where:
                - Keys: origin city (supplier city) for each order.
                - Values: list of strings representing orders (format as specified in section 4.1.4).
            - Order lists can be in any order.
            - No requirement on key ordering.

        Raises:
            Any exception during writing: Must be propagated to the caller.

        Notes:
            - The order origin city is the supplier city of the ordered product.
        """
        # TODO implement this method as instructed
        sorted_by_city = {}

        for order in self.orders.values():
            if order.product_id not in self.products:
                continue

            product = self.products[order.product_id]
            if product.supplier_id not in self.suppliers:
                continue

            supplier = self.suppliers[product.supplier_id]
            if supplier.city not in sorted_by_city:
                sorted_by_city[supplier.city] = []

            sorted_by_city[supplier.city].append(f"{order}")

        try:
            json.dump(sorted_by_city, out_file)
        except Exception as e:
            raise e

def load_system_from_file(path):
    """
    Load a MatamazonSystem from an input file.

    Args:
        path (str): Path to a text file containing customers, suppliers and products.

    Returns:
        MatamazonSystem: Initialized system with the data found in the file.

    Behavior:
        - The file lines contain objects in the format produced by export_system_to_file (section 4.2).
        - Lines may appear in any order (e.g., product lines can appear before supplier lines).
        - Illegal lines may be ignored.
        - If an exception occurs during the creation of any required object due to invalid data,
          the function should stop and propagate the exception (as specified).

    Notes:
        - The assignment hints that eval() may be used.
    """
    # TODO implement this function as instructed
    pass

# TODO all the main part here
