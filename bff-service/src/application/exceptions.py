class BFFServiceError(Exception):
    def __init__(self, status: int, message: str, entity: str = None):
        self.message = message
        self.status = status
        self.entity = entity
        super().__init__(self.message)
