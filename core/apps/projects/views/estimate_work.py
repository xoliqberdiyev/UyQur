from django.shortcuts import get_object_or_404

from rest_framework import generics, views
from rest_framework.response import Response

from core.apps.accounts.permissions.permissions import HasRolePermission
from core.apps.projects.models.project_estimate import EstimateWork
from core.apps.projects.serializers import estimate_work as serializers


class EstimateWorkCreateApiView(generics.GenericAPIView):
    serializer_class = serializers.EstimateWorkCreateSerializer
    queryset = EstimateWork.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = ['project', 'project_folder']

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'message': 'created!'}, status=201)
        return Response({'success': False, 'message': serializer.errors}, status=400)


class EstimateWorkUpdateApiView(generics.GenericAPIView):
    serializer_class = serializers.EstimateWorkUpdateSerializer
    queryset = EstimateWork.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = ['project', 'project_folder']

    def patch(self, request, id):
        estimate_work = get_object_or_404(EstimateWork, id=id)
        serializer = self.serializer_class(data=request.data, instance=estimate_work)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "Updated"}, status=200)
        return Response({'success': False, 'message': serializer.errors}, status=400)
    

class EstimateWorkDeleteApiView(views.APIView):
    permission_classes = [HasRolePermission]
    required_permissions = ['project']

    def delete(self, request, id):
        work = get_object_or_404(EstimateWork, id=id)
        work.delete()
        return Response({"success": True}, status=204)