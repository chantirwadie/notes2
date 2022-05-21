from django.shortcuts import render
from .models import Submit
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SubmitSerializer,SubmitAddSerializer
import traceback
from django.http import JsonResponse
import urllib3
import json
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework.pagination import PageNumberPagination
from django.db.models import CharField
from django.db.models import  Q
from django.db.models import Prefetch
from django.conf import settings

# Create your views here.
http = urllib3.PoolManager()


class SubmitAdd(APIView):
    parser_class = [MultiPartParser,FormParser]

    """ This class will handle the add of a new submit """
    def post(self, request):
   
        serializer = SubmitAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"data": serializer.data})


class GestionSubmit(APIView):
    """ This class will handle the CRUD OPERATIONS EXCEPT ADD"""
    def get(self, request, id):
        sub = Submit.objects.filter(pk=id).all()
        if sub:
            serializer = SubmitSerializer(sub, many=True)
            idEtudiant = serializer.data[0]['etudiant']
            url =settings.API_GATE_WAY+ '/api/v1/etudiant' 
            final_url = '/'.join([url, str(idEtudiant)])
            r = http.request('GET', final_url)
            data = json.loads(r.data)
            serializer.data[0]['etudiant']=data
            return Response({"Submit": serializer.data})
        return Response({"message" : "Ancun element existe avec l'identifiant donné"}, 400)

    def put(self,request, id):
        elementObject = Submit.objects.filter(pk=id).first()
        serializer = SubmitSerializer().update(elementObject, request.data)
        return Response(SubmitSerializer(serializer).data, 200)
       
    def delete(self, request, id):
        try:
            etudiantObject = Submit.objects.filter(pk=id).delete()
            return Response({"message" : "Deleted successfully"})
        except Exception as e:
            m = traceback.format_exc()    
            return Response({"message" : m}, 404)            



class GetAllSubmit(APIView,PageNumberPagination):

    # def get(self, request):
        
        # queryset = SubmitSerializer(Submit.objects.all(), many=True)
        # print(len(queryset.data))
        # for i in range(len(queryset.data)):
        #     idProfessseur = queryset.data[i]['etudiant']
        #     url = 'http://localhost:8000/api/v1/etudiant'  # no trailing /
        #     final_url = '/'.join([url, str(idProfessseur)])
        #     r = http.request('GET', final_url)
        #     data = json.loads(r.data)
        #     queryset.data[i]['etudiant']=data
        # return Response( queryset.data)
    page_size = 1000
    page_size_query_param = 'page_size'
    page_number = 1
    page_number_query_param = "page"
    
    def get_queryset(self):

        submits = Submit.objects.all().order_by('id')
        query = self.request.GET.get('query', None)
        if query:
            fields = [f for f in Submit._meta.fields if isinstance(f, CharField)]
            queries = [Q(**{f.name + "__icontains" : query}) for f in fields]
            qs = Q()
            for query in queries:
                qs = qs | query 
            submits = Submit.objects.filter(qs)
            
        queryset = SubmitSerializer(submits, many=True) 
        for i in range(len(queryset.data)):
            idProfessseur = queryset.data[i]['etudiant']
            url = settings.API_GATE_WAY+'/api/v1/etudiant'  # no trailing /
            final_url = '/'.join([url, str(idProfessseur)])
            r = http.request('GET', final_url)
            data = json.loads(r.data)
            queryset.data[i]['etudiant']=data
            
        return self.paginate_queryset(queryset.data, self.request)
        

    def get(self, request):
        submits = self.get_queryset()
        return self.get_paginated_response({"submits": submits})

    def post(self, request):
        ids = request.data.get('ids', None)
        if ids:
            Submit.objects.filter(id__in=ids).delete()
            delete_count = len(ids)
            return Response({"message" : "%d submits supprimés avec succès" % delete_count})

        return Response({"message" : "Veuillez fournir un identifiant"}, 400) 

    
