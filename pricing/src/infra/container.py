from src.application.usecases.calculate_order_total import CalculateOrderTotalUseCase
from src.domain.services.order_calculator import OrderCalculator
from src.infra.gateways.catalog.grpc_catalog import CatalogGrpcGateway
from src.interfaces.grpc.pricing_service import PricingService


def create_pricing_service_grpc(channel):
    catalog_gateway = CatalogGrpcGateway(channel)

    use_case = CalculateOrderTotalUseCase(
        catalog_gateway=catalog_gateway,
        order_calculator=OrderCalculator(),
    )

    return PricingService(use_case)
