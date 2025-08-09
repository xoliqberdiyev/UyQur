from django.shortcuts import get_object_or_404

from rest_framework import generics, views
from rest_framework.response import Response

from core.apps.accounts.permissions.permissions import HasRolePermission
from core.apps.projects.models.project_estimate import ProjectEstimate, EstimateProduct, EstimateWork
from core.apps.projects.serializers import project_estimate as serializers


class ProjectEstimateListApiView(generics.ListAPIView):
    serializer_class = serializers.ProjectEstimateListSerializer
    queryset = ProjectEstimate.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = ['project']


class ProjectEstimateCreateApiView(generics.GenericAPIView):
    serializer_class = serializers.ProjectEstimateCreateSerializer
    queryset = ProjectEstimate.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = ['project']

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, 'message': 'created'}, status=201)
        return Response({"success": True, "message":serializer.errors}, status=400)
    

class ProjectEstimateUpdateApiView(generics.GenericAPIView):
    serializer_class = serializers.ProjectEstimateUpdateSerializer
    queryset = ProjectEstimate.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = ['project']

    def patch(self, request, id):
        estimate = get_object_or_404(ProjectEstimate, id=id)
        serializer = self.serializer_class(data=request.data, instance=estimate)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'message': 'updated'}, status=200)
        return Response({'success': False, 'message': serializer.errors}, status=400)
    

class ProjectEstimateDeleteApiView(generics.GenericAPIView):
    queryset = ProjectEstimate.objects.all()
    serializer_class = None
    permission_classes = [HasRolePermission]
    required_permissions = ['project']

    def delete(self, request, id):
        estimte = get_object_or_404(ProjectEstimate, id=id)
        estimte.delete()
        return Response({"success": True, "message": "deleted"}, status=204)
    