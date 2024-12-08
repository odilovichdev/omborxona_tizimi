from rest_framework import serializers


class InputProductSerializer(serializers.Serializer):
    product_code = serializers.CharField()
    quantity = serializers.IntegerField()


class MaterialSerializer(serializers.Serializer):
    warehouse_id = serializers.IntegerField(allow_null=True)
    material_name = serializers.CharField()
    qty = serializers.FloatField()
    price = serializers.FloatField(allow_null=True)


class ProductResponseSerializer(serializers.Serializer):
    product_name = serializers.CharField()
    product_qty = serializers.IntegerField()
    product_materials = MaterialSerializer(many=True)
