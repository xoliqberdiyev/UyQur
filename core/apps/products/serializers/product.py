from django.db import transaction

from rest_framework import serializers

from core.apps.products.models import Product, Folder, SubFolder, Unity


class ProductListSerializer(serializers.ModelSerializer):
    unity = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'type', 'unity'
        ]

    def get_unity(self, obj):
        return {
            'id': obj.unity.id,
            'value': obj.unity.value
        } if obj.unity else None


class ProductSerializer(serializers.Serializer):
    name = serializers.CharField()
    type = serializers.ChoiceField(choices=Product.TYPE)
    unity_id = serializers.UUIDField()
    product_code = serializers.CharField(required=False)
    folder_id = serializers.UUIDField()
    sub_folder_id = serializers.UUIDField(required=False)

    def validate(self, data):
        folder = Folder.objects.filter(id=data.get('folder_id')).first()
        unity = Unity.objects.filter(id=data.get('unity_id')).first()
        if not folder:  
            raise serializers.ValidationError("Folder not found")
        if not unity:   
            raise serializers.ValidationError("Unity not found")
        if data.get("sub_folder_id"):
            sub_folder = SubFolder.objects.filter(id=data['sub_folder_id']).first()
            if not sub_folder:
                raise serializers.ValidationError("Sub Folder not found")
            data['sub_folder'] = sub_folder
        data['folder'] = folder
        data['unity'] = unity
        return data
    
    def create(self, validated_data):
        with transaction.atomic():
            return Product.objects.create(
                name=validated_data.get('name'),
                type=validated_data.get('type'),
                unity=validated_data.get('unity'),
                folder=validated_data.get('folder'),
                sub_folder=validated_data.get('sub_folder')
            )


class ProductUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    type = serializers.ChoiceField(choices=Product.TYPE)
    unity_id = serializers.UUIDField(required=False)
    product_code = serializers.CharField(required=False)
    folder_id = serializers.UUIDField(required=False)
    sub_folder_id = serializers.UUIDField(required=False)

    def validate(self, data):
        if data.get('folder_id'):
            folder = Folder.objects.filter(id=data.get('folder_id')).first()
            if not folder:  
                raise serializers.ValidationError("Folder not found")
            data['folder'] = folder
        if data.get('unity_id'):
            unity = Unity.objects.filter(id=data.get('unity_id')).first()
            if not unity:   
                raise serializers.ValidationError("Unity not found")
            data['unity'] = unity
        if data.get("sub_folder_id"):
            sub_folder = SubFolder.objects.filter(id=data['sub_folder_id'])
            if not sub_folder:
                raise serializers.ValidationError("Sub Folder not found")
            data['sub_folder'] = sub_folder
        return data
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.type = validated_data.get('type', instance.type)
        instance.unity = validated_data.get('unity', instance.unity)
        instance.folder = validated_data.get('folder', instance.folder)
        instance.sub_folder = validated_data.get('sub_folder', instance.sub_folder)
        instance.save()
        return instance
