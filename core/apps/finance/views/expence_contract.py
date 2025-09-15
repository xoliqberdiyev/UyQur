from django.utils.timezone import now
from django.db.models import Sum, Q, F

from django_filters.rest_framework.backends import DjangoFilterBackend

from rest_framework import generics, views, filters
from rest_framework.response import Response

from core.apps.finance.models import ExpenceContract
from core.apps.finance.serializers.expence_contract import ExpenceContractSerializer, ExpenceContractCreateSerializer
from core.apps.accounts.permissions.permissions import HasRolePermission


class ExpenceContractCreateApiView(generics.GenericAPIView):
    serializer_class = ExpenceContractCreateSerializer
    queryset = ExpenceContract.objects.all()
    permission_classes = [HasRolePermission]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    'success': True, 
                    'message': 'Expence Contract created successfully'
                },
                status=201
            )
        return Response(
            {
                'success': False,
                'message': 'Expence Contract create failed',
                'error': serializer.errors,
            },
            status=400
        )


class ExpenceContractListApiView(generics.GenericAPIView):
    serializer_class = ExpenceContractSerializer
    queryset = ExpenceContract.objects.select_related(
        'project_folder', 'project', 'user', 'expence_type', 'counterparty'
    )
    permission_classes = [HasRolePermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = [
        'user__full_name', 'project_folder__name', 'project__name', 'expence_type__name',
        'counterparty__name'
    ]

    def get(self, request):
        counterparty_id = request.query_params.get('counterparty')
        if counterparty_id:
            self.queryset = self.queryset.filter(counterparty=counterparty_id)
        
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        

class ExpenceContractStatisticsApiView(views.APIView):
    permission_classes = [HasRolePermission]
    
    def get(self, request):
        counterparty_id = request.query_params.get('counterparty')
        if counterparty_id:
            queryset = ExpenceContract.objects.filter(counterparty=counterparty_id)
        else:
            queryset = ExpenceContract.objects.all()
        today = now().date()
        usd = queryset.aggregate(
            plan_payments=Sum('price', filter=Q(currency='usd')),
            pending_payments=Sum(
                'price',
                filter=Q(date__gte=today) & Q(paid_price__isnull=True) & Q(currency='usd')
            ),
            paid_payments=Sum('paid_price', filter=Q(currency='usd')),
            overdue_payments=Sum(
                'price',
                filter=Q(date__lt=today) & Q(paid_price__lt=F('price')) & Q(currency='usd')
            )
        )
        uzs = queryset.aggregate(
            plan_payments=Sum('price', filter=Q(currency='uzs')),
            pending_payments=Sum(
                'price',
                filter=Q(date__gte=today) & Q(paid_price__isnull=True) & Q(currency='uzs')
            ),
            paid_payments=Sum('paid_price', filter=Q(currency='uzs')),
            overdue_payments=Sum(
                'price',
                filter=Q(date__lt=today) & Q(paid_price__lt=F('price')) & Q(currency='uzs')
            )
        )
        res = {
            'uzs': uzs,
            'usd': usd
        }
        return Response(res, status=200)
