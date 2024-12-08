from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import Product, ProductMaterial, Warehouse
from product.serializers import InputProductSerializer, ProductResponseSerializer


class ProductMaterialInfoAPIView(APIView):

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "products": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "product_code": openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                description="The unique code of the product."
                            ),
                            "quantity": openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                description="The quantity of the product."
                            )
                        },
                        required=["product_code", "quantity"]
                    ),
                    description="List of products with their codes and required quantities."
                )
            },
            required=["products"],
            example={
                "products": [
                    {
                        "product_code": 238923,
                        "quantity": 100
                    }
                ]
            }
        ),
        responses={
            200: openapi.Response(
                description="Materials and warehouses information for the requested product.",
                examples={
                    "application/json": {
                        "results": [
                            {
                                "product_name": "Koylak",
                                "product_qty": 100,
                                "product_materials": [
                                    {
                                        "warehouse_id": 1,
                                        "material_name": "Mato",
                                        "qty": 50,
                                        "price": 1500
                                    }
                                ]
                            }
                        ]
                    }
                }
            ),
            400: "Invalid input",
            404: "Product not found",
        }
    )
    def post(self, request, *args, **kwargs):

        input_info = InputProductSerializer(data=request.data.get("products"), many=True)

        if not input_info.is_valid():
            return Response(
                input_info.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        products_data = input_info.validated_data
        result = []

        for product_data in products_data:
            product_code = product_data['product_code']
            quantity = product_data['quantity']

            try:
                product = Product.objects.get(code=product_code)
            except Product.DoesNotExist:
                return Response(
                    {
                        "errors": f"Product with code {product_code} not found."
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            product_materials = ProductMaterial.objects.filter(product=product)

            product_info = {
                "product_name": product.name,
                "product_qty": quantity,
                "product_materials": []
            }

            for product_material in product_materials:
                material = product_material.material
                required_qty = product_material.quantity * quantity

                warehouse_data = self._get_material_from_warehouse(material, required_qty)

                product_info['product_materials'].extend(warehouse_data)

            result.append(product_info)

        response_serializer = ProductResponseSerializer(result, many=True)

        return Response(
            {
                "result": response_serializer.data,
            },
            status=status.HTTP_200_OK
        )


    def _get_material_from_warehouse(self, material, required_qty):
        warehouses = Warehouse.objects.filter(material=material).order_by("id")
        warehouse_data = []
        remaining_qty = required_qty

        for warehouse in warehouses:
            if remaining_qty <= 0:
                break

            if warehouse.remainder > 0:
                qty_to_take = min(warehouse.remainder, remaining_qty)
                warehouse_data.append(
                    {
                        "warehouse_id": warehouse.id,
                        "material_name": material.name,
                        "qty": qty_to_take,
                        "price": warehouse.price
                    }
                )
                remaining_qty -= qty_to_take

        if remaining_qty > 0:
            warehouse_data.append(
                {
                    "warehouse_id": None,
                    "material_name": material.name,
                    "qty": remaining_qty,
                    "price": None
                }
            )
        return warehouse_data




















