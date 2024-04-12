from contextlib import asynccontextmanager

import grpc
from fastapi import FastAPI
from src.infra.gateways.grpc_catalog import CatalogGrpcGateway
from src.infra.gateways.grpc_orders import OrdersGrpcGateway
from src.infra.gateways.grpc_pricing import PricingGrpcGateway


class GrpcGateways:
    # Orders
    orders_gateway: OrdersGrpcGateway = None
    orders_channel: grpc.aio.Channel = None

    # Catalog
    catalog_gateway: CatalogGrpcGateway = None
    catalog_channel: grpc.aio.Channel = None

    # Pricing
    pricing_gateway: PricingGrpcGateway = None
    pricing_channel: grpc.aio.Channel = None


gateways = GrpcGateways()


@asynccontextmanager
async def lifespan(app: FastAPI):

    gateways.orders_channel = grpc.aio.insecure_channel("orders-service:50053")
    gateways.orders_gateway = OrdersGrpcGateway(channel=gateways.orders_channel)

    gateways.catalog_channel = grpc.aio.insecure_channel("catalog-service:50051")
    gateways.catalog_gateway = CatalogGrpcGateway(channel=gateways.catalog_channel)

    gateways.pricing_channel = grpc.aio.insecure_channel("pricing-service:50054")
    gateways.pricing_gateway = PricingGrpcGateway(channel=gateways.pricing_channel)

    yield

    await gateways.orders_channel.close()
    await gateways.catalog_channel.close()
    await gateways.pricing_channel.close()


def get_order_gateway() -> OrdersGrpcGateway:
    return gateways.orders_gateway


def get_catalog_gateway() -> CatalogGrpcGateway:
    return gateways.catalog_gateway


def get_pricing_gateway() -> PricingGrpcGateway:
    return gateways.pricing_gateway
