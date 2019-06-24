from django.shortcuts import render

# from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from django.http import HttpResponse
# from rest_framework.authtoken.views import ObtainAuthToken

import os
import psycopg2

# Create your views here.

# @api_view()
# def bank_detail(request):
# 	""" Used to get the details of a particular bank provided IFSC code """

def homeview(request):

	return HttpResponse("""
		<h2>WELCOME TO BANK REST API</h2>
		<h4>add /api to the url to see the api endpoints .</h4>
		""")


class BankDetailAPIView(viewsets.ViewSet):

	permission_classes = (IsAuthenticated,)

	def list(self,request):

		ifsc = self.request.GET['ifsc']

		DATABASE_URL = os.environ['DATABASE_URL']

		conn = psycopg2.connect(DATABASE_URL, sslmode='require')

		# conn = psycopg2.connect("dbname='test1' user='postgres' host='localhost' password='harshit' connect_timeout=1 ")
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

		DATABASE_URL = os.environ['DATABASE_URL']

		conn = psycopg2.connect(DATABASE_URL, sslmode='require')

		# conn = psycopg2.connect("dbname='test1' user='postgres' host='localhost' password='harshit' connect_timeout=1 ")
		cur  = conn.cursor()

		cur.execute("SELECT * FROM infos2 WHERE bank_name='{}' AND city='{}'".format(bank_name,city))

		li = cur.fetchall()
		li_lenght = len(li)

		my_dict = {}
		my_dict['testlength']=li_lenght
		if li_lenght > 0 :
			a = offset
			if a <= (li_lenght-1):
				b=-1
				if limit <= (li_lenght-offset) :
					b = limit
				else :
					b = li_lenght-offset
				for k in range(offset,offset+b) :
					i = li[k]
					my_dict[a]=i
					a += 1
			else :
				my_dict['message']="offset out of limit .This number of items are not available ."
		else :
			my_dict['message']='No Banks'

		return Response(my_dict)