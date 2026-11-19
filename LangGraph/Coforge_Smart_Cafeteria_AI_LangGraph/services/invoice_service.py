from models.order_model import OrderRequest
from services.order_service import generate_invoice


def create_invoice(request: OrderRequest, validated_items):
    return generate_invoice(request, validated_items)
