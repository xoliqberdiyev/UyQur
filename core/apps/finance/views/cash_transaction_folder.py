from django.shortcuts import get_object_or_404

from rest_framework import generics, views, status
from rest_framework.response import Response

from core.apps.accounts.permissions.permissions import HasRolePermission
from core.apps.finance.models import CashTransactionFolder
from core.apps.finance.serializers.cash_transaction_folder import CashTransactionFolderSerializer


class CashTransactionCreateApiView(generics.GenericAPIView):
    serializer_class = CashTransactionFolderSerializer
    queryset = CashTransactionFolder.objects.all()
    permission_classes = [HasRolePermission]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    'success': True,
                    'message': 'Cash Transaction Folder created successfully'
                },
                status=status.HTTP_201_CREATED
            ) 
        return Response(
            {
                'success': False,
                'message': 'Cash Transaction Folder create failed',
                'error': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class CashTransactionFolderListApiView(generics.GenericAPIView):
    permission_classes = [HasRolePermission]
    queryset = CashTransactionFolder.objects.prefetch_related('cash_transactions')
    serializer_class = CashTransactionFolderSerializer

    def get(self, request):
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            ser = self.serializer_class(page, many=True)
            return self.get_paginated_response(ser.data)
        ser = self.serializer_class(self.queryset, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)


class CashTransactionFolderDeleteApiView(views.APIView):
    permission_classes = [HasRolePermission]
    
    def delete(self, request, id):
        folder = get_object_or_404(CashTransactionFolder, id=id)
        folder.delete()
        return Response(
            {
                'success': True,
                'message': 'Cash Transaction Folder successfully deleted!',
            },
            status=status.HTTP_204_NO_CONTENT
        )


class CashTransactionFolderUpdateApiView(generics.GenericAPIView):
    serializer_class = CashTransactionFolderSerializer
    queryset = CashTransactionFolder
    permission_classes = [HasRolePermission]

    def patch(self, request, id):
        folder = get_object_or_404(CashTransactionFolder, id=id)
        ser = self.serializer_class(data=request.data, instance=folder, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(
            {
                'success': True,
                'message': 'Cash Transaction Folder successfully updated!',
            },
            status=status.HTTP_200_OK
        )
