from django.http import HttpResponse
from companyinfo.query_rdf import getCompanyData, getAllCompany, getSomeCompany, getCompanyDataOnline
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

    for row in qres:
        name = row.str_name_label

    qresonline = getCompanyDataOnline(name)
    online_result = {}

    for result in qresonline["results"]["bindings"]:
        pred = str(result["pred"]["value"]).split("/")[-1]
        pred = pred.split("#")[-1]
        obj = str(result["obj"]["value"]).split("/")[-1]
        online_result[pred] = obj

    return render(request, 'companyinfo/company_details.html', {'qres': qres, 'online_result': online_result})