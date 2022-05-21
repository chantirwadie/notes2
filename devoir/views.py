from .models import Devoir
from rest_framework.views import APIView
from .serializers import DevoirSerializer,DevoirAddSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework.pagination import PageNumberPagination
from django.db.models import CharField
from django.db.models import  Q
from django.db.models import Prefetch
from submit.models import Submit
from django.conf import settings

import traceback
import urllib3
import json

import urllib3
import json
from rest_framework.parsers import MultiPartParser,FormParser

# Create your views here.
http = urllib3.PoolManager()


class DevoirAdd(APIView):
    parser_class = [MultiPartParser,FormParser]

    """ This class will handle the add of a new etudiant """
    def post(self, request):
   
        serializer = DevoirAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"data": serializer.data})


class GestionDevoir(APIView):
    """ This class will handle the CRUD OPERATIONS EXCEPT ADD"""
    def get(self, request, id):
        devoir = Devoir.objects.filter(pk=id).all()
        if devoir:
            serializer = DevoirSerializer(devoir, many=True)
            idProfessseur = serializer.data[0]['professeur']
            url = settings.API_GATE_WAY+'/api/v1/professeur' 
            final_url = '/'.join([url, str(idProfessseur)])
            r = http.request('GET', final_url)
            data = json.loads(r.data)
            serializer.data[0]['professeur']=data
            idElement = serializer.data[0]['element']
            print(idElement)
            url2 = settings.API_GATE_WAY+'/api/v2/element' 
            final_url2 = '/'.join([url2, str(idElement)])
            r2 = http.request('GET', final_url2)
            data2 = json.loads(r2.data)
            serializer.data[0]['element']=data2
            return Response({"devoir": serializer.data,"professeur":data,"element":data2})
        return Response({"message" : "Ancun element existe avec l'identifiant donné"}, 400)

    def put(self,request, id):
        elementObject = Devoir.objects.filter(pk=id).all()
        serializer = DevoirSerializer().update(elementObject, request.data)
        return Response(DevoirSerializer(serializer).data, 200)
       
    def delete(self, request, id):
        try:
            etudiantObject = Devoir.objects.filter(pk=id).delete()
            return Response({"message" : "Deleted successfully"})
        except Exception as e:
            m = traceback.format_exc()    
            return Response({"message" : m}, 404)            
class DevoirStats(APIView):
    def get(self, request):
        result = []
        url = settings.API_GATE_WAY+'/api/v1/professeur/all'  # no trailing /
        r = http.request('GET', url)
        data = json.loads(r.data)
        for i in range(len(data["results"]["professeurs"])):
            devoirs2 = Devoir.objects.filter(professeur=data["results"]["professeurs"][i]["id"])
            result.append({ "name" :data["results"]["professeurs"][i]["user"]["first_name"]+" "+data["results"]["professeurs"][i]["user"]["last_name"], "count" : devoirs2.count() })
        return Response(result)
class DevoirElementStats(APIView):
    def get(self, request, id):
        result = []
        url1 = settings.API_GATE_WAY+'/api/v2/inscription/all'  # no trailing /
        r = http.request('GET', url1)
        data2 = json.loads(r.data)
        for j in range(len(data2)):
            if(data2[j]["id"]==id):
                url = settings.API_GATE_WAY+'/api/v2/element/all'  # no trailing /
                r = http.request('GET', url)
                data = json.loads(r.data)
                for i in range(len(data["results"])):
                    if(data["results"][i]["module"]["filiere"]==data2[j]["filiere"]):
                        devoirs2 = Devoir.objects.filter(element=data["results"][i]["id"])
                        result.append({ "name" :data["results"][i]["nom"], "count" : devoirs2.count() })
        return Response(result)
class SubmitElementStats(APIView):
    def get(self, request, id):
        result = []
        url = settings.API_GATE_WAY+'/api/v2/element/all'  # no trailing /
        r = http.request('GET', url)
        data = json.loads(r.data)
        for j in range(len(data["results"])):
            if(data["results"][j]["professeur"]["id"]==id):
                devoirs = Devoir.objects.filter(element=data["results"][j]["id"])
                result.append({ "name" :data["results"][j]["nom"], "count" : devoirs.count() })
        return Response(result)
class SubmitProfStats(APIView):
    def get(self, request, id):
        result = []
        url = settings.API_GATE_WAY+'/api/v2/element/all'  # no trailing /
        r = http.request('GET', url)
        data = json.loads(r.data)
        for j in range(len(data["results"])):
            if(data["results"][j]["professeur"]["id"]==id):
                devoirs = Devoir.objects.filter(element=data["results"][j]["id"])
                for devoir in devoirs:
                    submit = Submit.objects.filter(devoir=devoir)
                    result.append({ "name" :devoir.sujet, "count" : submit.count() })
        return Response(result)


        

class GeneralStatApiView(APIView):

    def get(self, request):

        nbrDevoir = Devoir.objects.all().count()
        nbrSubmits = Submit.objects.all().count()
        return Response({
            'nbrDevoir': nbrDevoir,
            'nbrSubmits': nbrSubmits,

           
        })
        

class GetAllDevoir(APIView,PageNumberPagination):

    page_size = 1000
    page_size_query_param = 'page_size'
    page_number = 1
    page_number_query_param = "page"
    
    def get_queryset(self):

        devoirs = Devoir.objects.all().order_by('id')
        query = self.request.GET.get('query', None)
        if query:
            fields = [f for f in Devoir._meta.fields if isinstance(f, CharField)]
            queries = [Q(**{f.name + "__icontains" : query}) for f in fields]
            qs = Q()
            for query in queries:
                qs = qs | query 
            devoirs = Devoir.objects.filter(qs)
            
        queryset = DevoirSerializer(devoirs, many=True) 
        for i in range(len(queryset.data)):
            idProfessseur = queryset.data[i]['professeur']
            url = settings.API_GATE_WAY+'/api/v1/professeur'  # no trailing /
            final_url = '/'.join([url, str(idProfessseur)])
            r = http.request('GET', final_url)
            data = json.loads(r.data)
            queryset.data[i]['professeur']=data
            idElement = queryset.data[i]['element']
            url2 = settings.API_GATE_WAY+'/api/v2/element' 
            final_url2 = '/'.join([url2, str(idElement)])
            r2 = http.request('GET', final_url2)
            data2 = json.loads(r2.data)
            queryset.data[i]['element']=data2
            
        return self.paginate_queryset(queryset.data, self.request)
        

    def get(self, request):
        devoirs = self.get_queryset()
        return self.get_paginated_response({"devoirs": devoirs})

    def post(self, request):
        ids = request.data.get('ids', None)
        if ids:
            Devoir.objects.filter(id__in=ids).delete()
            delete_count = len(ids)
            return Response({"message" : "%d devoirs supprimés avec succès" % delete_count})

        return Response({"message" : "Veuillez fournir un identifiant"}, 400)     

    