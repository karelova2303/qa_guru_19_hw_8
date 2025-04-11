"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart


@pytest.fixture
def product_book() -> Product:
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def product_flower() -> Product:
    return Product("flower", 500, "This is a flower", 1000)


@pytest.fixture
def product_toy() -> Product:
    return Product("toy", 1000, "This is a toy", 1000)


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity_positive(self, product_book: Product):
        # Напишите проверки на метод check_quantity
        assert product_book.check_quantity(product_book.quantity)

    def test_product_check_quantity_negative(self, product_book: Product):
        # Напишите проверки на метод check_quantity
        assert not product_book.check_quantity(product_book.quantity + 1)

    def test_product_buy_tenth(self, product_book: Product):
        # Напишите проверки на метод buy
        buy_quantity = product_book.quantity / 10
        quantity_before = product_book.quantity

        product_book.buy(buy_quantity)

        assert product_book.quantity == quantity_before - buy_quantity

    def test_product_buy_more_than_available(self, product_book: Product):
        # Напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError):
            product_book.buy(product_book.quantity + 1)


@pytest.fixture
def cart() -> Cart:
    return Cart()


class TestCart:
    """
    Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    # Тест на добавления в корзину товара одного вида
    def test_add_product_in_cart(self, cart: Cart, product_book: Product):
        book_count = 100

        cart.add_product(product_book, book_count)
        assert cart.products[product_book] == book_count

    # Тест на добавления в корзину товара одного вида дважды, разного количества
    def test_add_double_product_in_cart(self, cart: Cart, product_book: Product):
        book_count_one = 300
        book_count_two = 500

        cart.add_product(product_book, book_count_one)
        cart.add_product(product_book, book_count_two)
        actual_result = book_count_one + book_count_two

        assert cart.products[product_book] == actual_result

    # Тест на добавления товара в корзину больше, чем есть на остатке
    def test_add_more_product_in_cart(self, cart: Cart, product_book: Product):
        with pytest.raises(ValueError):
            cart.add_product(product_book, product_book.quantity + 1)

    # Тест на добавления товара в корзину с количеством 0
    def test_add_zero_product_in_cart(self, cart: Cart, product_book: Product):
        with pytest.raises(ValueError):
            cart.add_product(product_book, 0)

    # Тест на добавления в корзину товаров разного вида и количества
    def test_add_two_products_in_cart(self, cart: Cart, product_book: Product, product_flower: Product):
        book_count = 300
        flower_count = 500

        cart.add_product(product_book, book_count)
        cart.add_product(product_flower, flower_count)

        assert cart.products[product_book] == book_count
        assert cart.products[product_flower] == flower_count

    # Тест на удаление из корзины всех товаров
    def test_remove_all_product(self, cart: Cart, product_book: Product):
        cart.add_product(product_book, 100)
        cart.remove_product(product_book)
        assert cart.products == {}

    # Тест на удаление из корзины товаров больше, чем добавлено
    def test_remove_more_product(self, cart: Cart, product_book: Product):
        cart.add_product(product_book, 100)
        cart.remove_product(product_book, cart.products[product_book] + 1)
        assert cart.products == {}

    # Тест на удаления из корзины определенного количества товара
    def test_remove_count_product(self, cart: Cart, product_book: Product):
        cart.add_product(product_book, 500)
        cart.remove_product(product_book, 100)
        assert cart.products[product_book] == 400

    # Тест на удаление из корзины товара, который не был добавлен
    def test_remove_absent_product(self, cart: Cart, product_book: Product, product_flower: Product):
        cart.add_product(product_book, 500)
        with pytest.raises(ValueError):
            cart.remove_product(product_flower)

    # Тест на полную очистку корзины, если добавлен 1 товар
    def test_clear_cart_one_product(self, cart: Cart, product_book: Product):
        cart.add_product(product_book, 100)
        cart.clear()
        assert not cart.products

    # Тест на полную очистку корзины, если добавлено 3 товара
    def test_clear_cart_three_products(self, cart: Cart, product_book: Product, product_flower: Product,
                                       product_toy: Product):
        cart.add_product(product_book, 100)
        cart.add_product(product_flower, 400)
        cart.add_product(product_toy, 200)

        cart.clear()

        assert not cart.products

    # Тест на полную очистку корзины, если корзина пустая
    def test_clear_empty_cart(self, cart: Cart):
        cart.clear()
        assert not cart.products

    # Тест на расчет общей стоимости товара в корзине
    def test_get_total_price_one_product(self, cart: Cart, product_book: Product):
        book_count = 300

        cart.add_product(product_book, book_count)
        total_price = cart.get_total_price()
        actual_result = product_book.price * book_count

        assert actual_result == total_price

    # Тест на расчет общей стоимости двух товаров в корзине
    def test_get_total_price_two_products(self, cart: Cart, product_book: Product, product_flower: Product):
        book_count = 300
        flower_count = 500

        cart.add_product(product_book, book_count)
        cart.add_product(product_flower, flower_count)
        total_price = cart.get_total_price()
        actual_result = product_book.price * book_count + product_flower.price * flower_count

        assert actual_result == total_price

    # Тест на расчет общей стоимости товара в пустой корзине
    def test_get_total_price_empty_cart(self, cart: Cart, product_book: Product):
        total_price = cart.get_total_price()
        assert total_price == 0

    # Тест на покупку товара
    def test_buy_product(self, cart: Cart, product_book: Product):
        book_count_on_storage = product_book.quantity
        count_book_to_buy = 100
        cart.add_product(product_book, count_book_to_buy)

        cart.buy()
        actual_result = book_count_on_storage - count_book_to_buy

        assert actual_result == product_book.quantity
        assert not cart.products

    # Тест на покупку двух видов товара
    def test_buy_two_products(self, cart: Cart, product_book: Product, product_flower: Product):
        book_count_on_storage = product_book.quantity
        count_book_to_buy = 100
        flower_count_on_storage = product_flower.quantity
        count_flower_to_buy = 200
        cart.add_product(product_book, count_book_to_buy)
        cart.add_product(product_flower, count_flower_to_buy)

        cart.buy()

        assert product_book.quantity == book_count_on_storage - count_book_to_buy
        assert product_flower.quantity == flower_count_on_storage - count_flower_to_buy
        assert not cart.products

    # Тест на покупку товара большего количества, чем есть на остатке
    def test_buy_more_products(self, cart: Cart, product_book: Product):
        cart.add_product(product_book, product_book.quantity)
        cart.products[product_book] += 1

        with pytest.raises(ValueError):
            cart.buy()

    # Тест на покупку товара c количеством 0
    def test_buy_zero_product(self, cart: Cart, product_book: Product):
        book_count_on_storage = product_book.quantity
        cart.add_product(product_book, 1)
        cart.products[product_book] = 0

        cart.buy()

        assert product_book.quantity == book_count_on_storage
        assert not cart.products
