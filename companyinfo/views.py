from django.http import HttpResponse
from companyinfo.query_rdf import getCompanyData, getAllCompany, getSomeCompany
from .models import Question
from django.shortcuts import render

def index(request):
    qres = getAllCompany()
    return render(request, 'companyinfo/index.html', {'qres': qres})

def search(request):
    param = request.POST['companyname']
    qres = getSomeCompany(param)
    return render(request, 'companyinfo/index.html', {'qres': qres})

def info(request, rdf_object):
    qres = getCompanyData(rdf_object)
    return render(request, 'companyinfo/company_details.html', {'qres': qres})