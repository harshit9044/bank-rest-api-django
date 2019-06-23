from django.shortcuts import render

# from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
# from rest_framework.authtoken.views import ObtainAuthToken


import psycopg2

# Create your views here.

# @api_view()
# def bank_detail(request):
# 	""" Used to get the details of a particular bank provided IFSC code """


class BankDetailAPIView(viewsets.ViewSet):

	permission_classes = (IsAuthenticated,)

	def list(self,request):

		ifsc = self.request.GET['ifsc']

		conn = psycopg2.connect("dbname='test1' user='postgres' host='localhost' password='harshit' connect_timeout=1 ")
		cur  = conn.cursor()

		cur.execute("SELECT * FROM infos2 WHERE ifsc='{}';".format(ifsc))
		obj = cur.fetchall()
		ifsc = obj[0][0]
		bank_id = obj[0][1]
		branch  = obj[0][2]
		address = obj[0][3]
		city    = obj[0][4]
		district= obj[0][5]
		state   = obj[0][6]
		bank_name=obj[0][7]
		# print(ifsc)
		# print(obj[0][0],obj[0][1])
		# print(type(obj))
		
		return Response({
				'Bank Name':bank_name,
				"IFSC":ifsc,
				'Bank ID':bank_id,
				'BRANCH':branch,
				'City':city,
				'District':district,
				'State':state,
				'Address':address,
			})


class AllBranchesAPIView(viewsets.ViewSet):

	permission_classes = (IsAuthenticated,)

	def list(self,request):
		bank_name = self.request.GET['bank-name']
		city      = self.request.GET['city']
		limit     = int(self.request.GET['limit'])
		offset    = int(self.request.GET['offset'])

		conn = psycopg2.connect("dbname='test1' user='postgres' host='localhost' password='harshit' connect_timeout=1 ")
		cur  = conn.cursor()

		cur.execute("SELECT * FROM infos2 WHERE bank_name='{}' AND city='{}'".format(bank_name,city))

		li = cur.fetchall()

		my_dict = {}
		if li is not None :
			a = offset
			for k in range(offset,offset+limit) :
				i = li[k]
				my_dict[a]=i
				a += 1
		else :
			my_dict['message']='No Banks'

		return Response(my_dict)