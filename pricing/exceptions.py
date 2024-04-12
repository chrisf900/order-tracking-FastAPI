class OrderNotFoundError(Exception):
    pass


class OrderDetailNotFoundError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class UserDBError(Exception):
    pass


class EmailAlreadyRegisteredError(Exception):
    pass


class InvalidDeliveryStatusTransition(Exception):
    pass


class AddProductsIsNotAvailable(Exception):
    pass


class DeleteProductsIsNotAvailable(Exception):
    pass


class CancelOrderIsNotAvailable(Exception):
    pass
