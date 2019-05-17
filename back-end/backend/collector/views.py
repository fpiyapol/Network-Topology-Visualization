from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Device, Link, Management
from .collector import Collector

from .serializers import DeviceSerializer, LinkSerializer,  ManagementSerializer
from .ctest import CTest

class DeviceView(APIView):
    def get(self, request):
        """ Request GET method """
        devices = Device.objects.all()
        serializer = DeviceSerializer(devices, many=True)
        return Response({"devices": serializer.data})

    def post(self, request):
        """ Request POST method """
        device = request.data.get('device')
        print(device)
        mSerializer = ManagementSerializer(data=device)
        if mSerializer.is_valid(raise_exception=True):
            m_saved = mSerializer.save()
        return Response({"success": "Management '{}' created successfully".format(m_saved.ip_addr)})

    # def put(self, request, pk):
    #     saved_device = get_object_or_404(Article.objects.all(), pk=pk)
    #     data = request.data.get('article')
    #     serializer = ArticleSerializer(instance=saved_device, data=data, partial=True)
    #     if serializer.is_valid(raise_exception=True):
    #         saved_device=serializer.save()
    #     return Response({"success": "Device '{}' updated successfully".format(saved_device.title)})


    # def delete(self, request, pk):
    #     # Get object with this pk
    #     print('pk', pk)
    #     device=get_object_or_404(Device.objects.all(), pk=pk)
    #     device.delete()
    #     return Response({"message": "Device with id `{}` has been deleted.".format(pk)}, status=204)

class UpdateView(APIView):
    def get(self, request):
        """ Request GET method """
        collect = Collector
        collect.main(collect)
        devices = Device.objects.all()
        serializer = DeviceSerializer(devices, many=True)
        return Response({"devices": serializer.data})
