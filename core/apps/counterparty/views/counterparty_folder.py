from django.shortcuts import get_object_or_404

from rest_framework import generics, views
from rest_framework.response import Response

from core.apps.counterparty.models import CounterpartyFolder
from core.apps.counterparty.serializers import counterparty_folder as serializers
from core.apps.accounts.permissions.permissions import HasRolePermission


class CounterpartyFolderListApiView(generics.GenericAPIView):
    serializer_class = serializers.CounterpartyFolderListSerializer
    queryset = CounterpartyFolder.objects.all()
    permission_classes = [HasRolePermission]
    pagination_class = None

    def get(self, request):
        folders = self.get_queryset()
        serializer = self.serializer_class(folders, many=True)
        return Response(serializer.data, status=200)
    

class CounterpartyCreateApiView(generics.GenericAPIView):
    serializer_class = serializers.CounterpartyFolderCreateSerializer
    queryset = CounterpartyFolder.objects.all()
    permission_classes = [HasRolePermission]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'success': True, 'message': 'created'},
                status=201
            )
        return Response(
            {'success': False, 'message': serializer.errors},
            status=400
        )


class CounterpartyDeleteApiView(views.APIView):
    permission_classes = [HasRolePermission]

    def delete(self, request, id):
        counterparty_folder = get_object_or_404(CounterpartyFolder, id=id)
        counterparty_folder.delete()
        return Response(
            {'success': True, 'message': 'counterparty folder deleted'},
            status=204
        )
    

class CounterpartyUpdateApiView(generics.UpdateAPIView):
    queryset = CounterpartyFolder.objects.all()
    serializer_class = serializers.CounterpartyFolderListSerializer
    lookup_field = 'id'
    permission_classes = [HasRolePermission]