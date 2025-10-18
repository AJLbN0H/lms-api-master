from config.settings import STRIPE_API_KEY
import stripe

from materials.models import Course

stripe.api_key = STRIPE_API_KEY


def create_product(course_id):
    """Метод создания продукта."""

    course = Course.objects.get(id=course_id)
    product = stripe.Product.create(name=course.name)
    product["price"] = course.price
    return product


def create_price(price_course):
    """Метод создания цены."""

    return stripe.Price.create(
        currency="rub",
        unit_amount=price_course * 100,
        product_data={"name": "Payments"},
    )


def create_session(price):
    """Метод создания сессии."""

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
