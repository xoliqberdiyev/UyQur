from django.shortcuts import get_object_or_404

from rest_framework import generics, views
from rest_framework.response import Response

from core.apps.accounts.permissions.permissions import HasRolePermission
from core.apps.finance.models import PaymentType
from core.apps.finance.serializers.payment_type import PaymentTypeSerializer


class PaymentTypeCreateApiView(generics.GenericAPIView):
    serializer_class = PaymentTypeSerializer
    queryset = PaymentType.objects.all()
    permission_classes = [HasRolePermission]

    def post(self, request):
        ser = self.serializer_class(data=request.data)
        if ser.is_valid(raise_exception=True):
            ser.save()
            return Response({'success': True}, status=201)
        return Response(ser.errors, status=400)
    

class PaymentListApiView(views.APIView):
    permission_classes = [HasRolePermission]

    def get(self, request):
        queryset = PaymentType.objects.all()
        ser = PaymentTypeSerializer(queryset, many=True)
        return Response(ser.data, status=200)


class PaymentDeleteApiView(views.APIView):
    permission_classes = [HasRolePermission]

    def delete(self, request, id):
        obj = get_object_or_404(PaymentType, id=id)
        obj.delete()
        return Response(status=204)
    

class PaymentUpdateApiView(generics.GenericAPIView):
    permission_classes = [HasRolePermission]
    queryset = PaymentType.objects.all()
    serializer_class = PaymentTypeSerializer

    def patch(self, request, id):
        obj = get_object_or_404(PaymentType, id=id)
        ser = self.serializer_class(data=request.data, instance=obj, partial=True)
        if ser.is_valid():
            ser.save()
            return Response({'success': True}, status=200)
        return Response(ser.errors, status=400)


    