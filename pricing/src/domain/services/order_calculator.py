from typing import List

from src.application.dtos.order import OrderItemDTO
from src.application.dtos.product import ProductForPricingDTO


class OrderCalculator:
    def calculate_total(
        self,
        items: List[OrderItemDTO],
        catalog_products: List[ProductForPricingDTO],
    ) -> float:
        price_map = {product.id: product.price for product in catalog_products}

        return sum(
            item.quantity * price_map[item.product_id]
            for item in items
            if item.product_id in price_map
        )
