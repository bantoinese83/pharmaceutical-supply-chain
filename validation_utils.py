import datetime
from voluptuous import Schema, All, Length, Match, Range, Invalid


class ValidationError(Exception):
    pass


class Validator:
    @staticmethod
    def validate(schema, data):
        try:
            return schema(data)
        except Invalid:
            raise ValidationError(f"Invalid data: {data}")

    @staticmethod
    def validate_product_id(product_id):
        schema = Schema(All(str, Length(min=6, max=10), Match(r"^[A-Za-z0-9]{6,10}$")))
        return Validator.validate(schema, product_id)

    @staticmethod
    def validate_transaction_detail(transaction_detail):
        schema = Schema(All(str, Length(min=1)))
        return Validator.validate(schema, transaction_detail)

    @staticmethod
    def validate_id(id):
        schema = Schema(All(int, Range(min=0)))
        return Validator.validate(schema, id)

    @staticmethod
    def validate_quantity(quantity):
        schema = Schema(All(int, Range(min=0)))
        return Validator.validate(schema, quantity)

    @staticmethod
    def validate_price(price):
        schema = Schema(All(float, Range(min=0)))
        return Validator.validate(schema, price)

    @staticmethod
    def validate_address(address):
        schema = Schema(All(str, Length(min=1)))
        return Validator.validate(schema, address)

    @staticmethod
    def validate_date(date):
        schema = Schema(All(str, Match(r"^\d{4}-\d{2}-\d{2}$")))
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
            return Validator.validate(schema, date)
        except ValueError:
            raise ValidationError(f"Invalid date: {date}")

    # Use validate_id for supplier_id and customer_id
    validate_supplier_id = validate_id
    validate_customer_id = validate_id
