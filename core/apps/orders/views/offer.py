from django.shortcuts import get_object_or_404

from rest_framework import generics, views
from rest_framework.response import Response

from core.apps.shared.paginations.custom import PageNumberPagination
from core.apps.accounts.permissions.permissions import HasRolePermission
from core.apps.orders.serializers import offer as serializers
from core.apps.orders.models import Offer


class OffersCreateApiView(generics.GenericAPIView):
    permission_classes = [HasRolePermission]
    required_permissions = ['offer']
    queryset = Offer.objects.all()
    serializer_class = serializers.MultipleOfferCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Offers created!"
                },
                status=201
            )


class OfferListApiView(generics.GenericAPIView):
    permission_classes = [HasRolePermission]
    queryset = Offer.objects.all()
    required_permissions = ['offer']
    serializer_class = serializers.OfferListSerializer

    def get(self, request):
        offers = Offer.objects.all()
        page = self.paginate_queryset(offers)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(offers, many=True)
        return Response(serializer.data, status=200)
    

class OfferUpdateApiView(generics.GenericAPIView):
    serializer_class = serializers.OfferUpdateSerializer
    queryset = Offer.objects.all()
    lookup_field = 'id'
    permission_classes = [HasRolePermission]
    required_permissions = ['offer']

    def put(self, request, id):
        offer = get_object_or_404(Offer, id=id)
        serializer = self.serializer_class(data=request.data, instance=offer)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    'success': True,
                    "message": "Offer successfully updated!"
                },
                status=200
            )
    
    def patch(self, request, id):
        offer = get_object_or_404(Offer, id=id)
        serializer = self.serializer_class(data=request.data, instance=offer, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    'success': True,
                    "message": "Offer successfully updated!"
                },
                status=200
            )
        
    
class OfferDeleteApiView(views.APIView):
    permission_classes = [HasRolePermission]
    required_permissions = ['offer']

    def delete(self, request, id):
        offer = get_object_or_404(Offer, id=id)
        offer.delete()
        return Response({'success': True}, status=204)