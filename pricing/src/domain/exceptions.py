class DomainError(Exception):
    pass


class InvalidTotalAmount(DomainError):
    pass


class ProductNotFound(DomainError):
    pass
