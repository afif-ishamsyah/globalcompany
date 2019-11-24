from django.http import HttpResponse
from companyinfo.query_rdf import getCompanyData, getAllCompany, getSomeCompany, getCompanyDataOnline
from .models import Question
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, InvalidPage

def index(request):
    return render(request, 'companyinfo/index.html')


def search(request):

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    param = request.GET['companyname']

    qres = getSomeCompany(param)

    listCompany = []
    for value in qres["results"]["bindings"]:
        # image = getImageThumbnail(value["str_name_label"]["value"], value["domainurl"]["value"])
        # image = ''
        # listCompany.append({'id': value["id"]["value"], 'name': value["str_name_label"]["value"], 'country': value["str_country_label"]["value"], 'linkedin': value["linkedinurl"]["value"], 'img_thumbnail': image  })
        listCompany.append({'id': value["id"]["value"], 'name': value["str_name_label"]["value"], 'country': value["str_country_label"]["value"], 'linkedin': value["linkedinurl"]["value"] })

    paginator = Paginator(listCompany, 24)

    try:
        company = paginator.page(page)
    except(EmptyPage, InvalidPage):
        company = paginator.page(1)

    index = company.number - 1  
    max_index = len(paginator.page_range)
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    page_range = list(paginator.page_range)[start_index:end_index]

    return render(request, 'companyinfo/company_list.html', {'company': company, 'page_range': page_range, 'param': param, 'total_results':len(listCompany), 'query':param+""}
)

# def getImageThumbnail(name, web):
#     qresonline = getThumbnail(name, web)
#     image = ""
#     for result in qresonline["results"]["bindings"]:
#         image = result["str_thumbnail"]["value"]
#     return image

def info(request, rdf_object):
    local_result = {}
    online_result = {}
    name = ''
    web = ''
    qres = getCompanyData(rdf_object)

    for row in qres["results"]["bindings"]:
        name = row["str_name_label"]["value"]
        local_result['name'] = str(row["str_name_label"]["value"]).title()
        local_result['country_label'] = row["str_country_label"]["value"]
        local_result['industry_label'] = row["str_industry_label"]["value"]
        local_result['year'] = row["str_year"]["value"]
        local_result['size'] = row["str_size"]["value"]
        local_result['locality_label'] = row["str_locality_label"]["value"]
        local_result['current'] = row["str_current"]["value"]
        local_result['total'] = row["str_total"]["value"]
        local_result['linkedinurl'] = ''
        if(str(row["linkedinurl"]["value"]) != '-'):
            local_result['linkedinurl'] = 'https://' + str(row["linkedinurl"]["value"])

        local_result['domainurl'] = ''
        if(str(row["domainurl"]["value"]) != '-'):
            local_result['domainurl'] = 'https://' + str(row["domainurl"]["value"])

        web = str(row["domainurl"]["value"])

    qresonline = getCompanyDataOnline(name, web)
    
    for result in qresonline["results"]["bindings"]:
        if str(result["str_topic"]["value"]) != '-': online_result['topic'] = result["str_topic"]["value"]
        if str(result["str_wikipageid"]["value"]) != '-': online_result['wikipageid'] = result["str_wikipageid"]["value"]
        if str(result["str_latitude"]["value"]) != '-': online_result['latitude'] = result["str_latitude"]["value"]
        if str(result["str_longitude"]["value"]) != '-': online_result['longitude'] = result["str_longitude"]["value"]
        if str(result["str_abstract"]["value"]) != '-':online_result['abstract'] = result["str_abstract"]["value"]
        if str(result["str_assets"]["value"]) != '0': online_result['assets'] = '${:,.2f}'.format(float(result["str_assets"]["value"]))
        if str(result["str_equity"]["value"]) != '0': online_result['equity'] = '${:,.2f}'.format(float(result["str_equity"]["value"]))
        if str(result["str_location"]["value"]) != '-': online_result['location'] = str(result["str_location"]["value"]).split("/")[-1].replace('_',' ')
        if str(result["str_netincome"]["value"]) != '0': online_result['netincome'] = '${:,.2f}'.format(float(result["str_netincome"]["value"]))
        if str(result["str_operatingincome"]["value"]) != '0': online_result['operatingincome'] = '${:,.2f}'.format(float(result["str_operatingincome"]["value"]))
        if str(result["str_revenue"]["value"]) != '0': online_result['revenue'] = '${:,.2f}'.format(float(result["str_revenue"]["value"]))
        if str(result["str_areaserved"]["value"]) != '-': online_result['areaserved'] = result["str_areaserved"]["value"]
        if str(result["str_thumbnail"]["value"]) != '-': online_result['thumbnail'] = result["str_thumbnail"]["value"]

    return render(request, 'companyinfo/company_details_alt.html', {'local_result': local_result, 'online_result': online_result})
