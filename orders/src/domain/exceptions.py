class DomainError(Exception):
    pass


class OrderCreationError(DomainError):
    pass


class OrderDetailCreationError(DomainError):
    pass


class OrderNotFoundError(DomainError):
    pass


class OrderStatusNotUpdatedError(DomainError):
    pass


class OrderDetailNotFoundError(DomainError):
    pass


class InvalidTotalAmount(DomainError):
    pass


class InvalidStatusName(DomainError):
    pass


class InvalidDeliveryStatusTransition(DomainError):
    pass


class CancelOrderIsNotAvailable(DomainError):
    pass
