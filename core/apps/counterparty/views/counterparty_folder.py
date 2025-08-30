from rest_framework import generics
from rest_framework.response import Response

from core.apps.counterparty.models import CounterpartyFolder
from core.apps.counterparty.serializers import counterparty_folder as serializers
from core.apps.accounts.permissions.permissions import HasRolePermission


class CounterpartyFolderListApiView(generics.GenericAPIView):
    serializer_class = serializers.CounterpartyFolderListSerializer
    queryset = CounterpartyFolder.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = []

    def get(self, request):
        folders = self.queryset
        serializer = self.serializer_class(folders, many=True)
        return Response(serializer.data, status=200)
    

class CounterpartyCreateApiView(generics.GenericAPIView):
    serializer_class = serializers.CounterpartyFolderCreateSerializer
    queryset = CounterpartyFolder.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializers.save()
            return Response(
                {'success': True, 'message': 'created'},
                status=201
            )
        return Response(
            {'success': False, 'message': serializer.errors},
            status=400
        )
