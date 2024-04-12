import datetime
from typing import Type

from src.domain.exceptions import InvalidDeliveryStatusTransition, InvalidStatusName


class DeliveryStatus:
    state_name = ""

    def __init__(self, order_instance):
        self.order = order_instance

    def new_state(self, state) -> None:
        self.__class__ = state

    def action(self, state) -> None:
        raise NotImplementedError()

    def __str__(self):
        return self.state_name

    def _set_status(self, new_status) -> None:
        """saves the new status"""

        if new_status.upper() == self.order.delivery_status:
            raise InvalidDeliveryStatusTransition()

        self.order.delivery_status = new_status
        self.order.updated_at = datetime.datetime.now(datetime.UTC)


class Draft(DeliveryStatus):
    state_name = "DRAFT"
    valid_transitions = ["IN_PROGRESS", "CANCELLED"]

    def action(self, state):
        if state in self.valid_transitions:
            self._set_status(new_status=state)
            return state
        return None


class InProgress(DeliveryStatus):
    state_name = "IN_PROGRESS"
    valid_transitions = ["DELIVERED", "CANCELLED"]

    def action(self, state):
        if state in self.valid_transitions:
            self._set_status(new_status=state)
            return state
        return None


class PreparingForDelivery(DeliveryStatus):
    state_name = "PREPARING_FOR_DELIVERY"
    valid_transitions = ["IN_PROGRESS", "CANCELLED"]

    def action(self, state):
        if state in self.valid_transitions:
            self._set_status(new_status=state)
            return state
        return None


class Delivered(DeliveryStatus):
    state_name = "DELIVERED"

    def action(self, state):
        self._set_status(new_status=state)


class Cancelled(DeliveryStatus):
    state_name = "CANCELLED"

    def action(self, state):
        self._set_status(new_status=state)


class DeliveryStateMachine:
    STATE_MAPPING = {
        "DRAFT": Draft,
        "IN_PROGRESS": InProgress,
        "PREPARING_FOR_DELIVERY": PreparingForDelivery,
        "DELIVERED": Delivered,
        "CANCELLED": Cancelled,
    }

    def __init__(self, state: str, order):
        self.order = order
        self.state = self.get_state_class(state)(order_instance=order)

    def change(self, new_state) -> None:
        self.state.action(new_state)

    def get_state_class(self, state: str) -> Type[DeliveryStatus]:
        try:
            return self.STATE_MAPPING[state]
        except KeyError:
            raise InvalidStatusName()
