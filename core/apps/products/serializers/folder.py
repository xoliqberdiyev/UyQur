from rest_framework import serializers

from core.apps.products.models.folder import Folder, SubFolder


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['id', 'name']
        extra_kwargs = {'id': {'read_only': True}}

    def create(self, validated_data):
        return Folder.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
    

class SubFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubFolder
        fields = ['id', 'name', 'folder']
        extra_kwargs = {'id': {'read_only': True}, "folder": {"write_only": True}}

    def create(self, validated_data):
        return SubFolder.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.folder = validated_data.get('folder', instance.folder)
        instance.save()
        return instance