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
    local_result = {}
    online_result = {}
    name = ''
    web = ''
    qres = getCompanyData(rdf_object)

    for row in qres:
        name = row.str_name_label
        local_result['name'] = str(row.str_name_label).title()
        local_result['country_label'] = row.str_country_label
        local_result['industry_label'] = row.str_industry_label
        local_result['year'] = row.str_year
        local_result['size'] = row.str_size
        local_result['locality_label'] = row.str_locality_label
        local_result['current'] = row.str_current
        local_result['total'] = row.str_total
        local_result['linkedinurl'] = ''
        if(str(row.linkedinurl) != ''):
            local_result['linkedinurl'] = 'https://' + str(row.linkedinurl)

        local_result['domainurl'] = ''
        if(str(row.domainurl) != ''):
            local_result['domainurl'] = 'https://' + str(row.domainurl)

        web = str(row.domainurl)

    qresonline = getCompanyDataOnline(name, web)
    
    for result in qresonline["results"]["bindings"]:
        online_result['topic'] = result["str_topic"]["value"]
        online_result['wikipageid'] = result["str_wikipageid"]["value"]
        online_result['latitude'] = result["str_latitude"]["value"]
        online_result['longitude'] = result["str_longitude"]["value"]
        online_result['abstract'] = result["str_abstract"]["value"]
        online_result['assets'] = '${:,.2f}'.format(float(result["str_assets"]["value"]))
        online_result['equity'] = '${:,.2f}'.format(float(result["str_equity"]["value"]))
        online_result['location'] = str(result["str_location"]["value"]).split("/")[-1]
        online_result['netincome'] = '${:,.2f}'.format(float(result["str_netincome"]["value"]))
        online_result['operatingincome'] = '${:,.2f}'.format(float(result["str_operatingincome"]["value"]))
        online_result['revenue'] = '${:,.2f}'.format(float(result["str_revenue"]["value"]))
        online_result['areaserved'] = result["str_areaserved"]["value"]
        online_result['thumbnail'] = result["str_thumbnail"]["value"]

    return render(request, 'companyinfo/company_details.html', {'local_result': local_result, 'online_result': online_result})
