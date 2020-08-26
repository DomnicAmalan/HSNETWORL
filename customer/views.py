from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import Context, loader
import base64
from .helpers import db
import json
from django.contrib import messages

# Create your views here.
def signin(request):
    return render(request, 'signin.html', {'poll': "p"})

def phoneAuth(request):
    return render(request, 'phoneauth.html')

def dashboard(request):
    return render(request, 'Dashboard.html', {"options": ['AADHAR', 'COMMUNITY CERTIFICATE', 'DRIVING LICENCE', 'ENCUMBRANCE CERTIFICATE', 'FSSAI', 'GST', 'RATION', 'PAN CARD', 'INCOME CERTIFICATE', 'TNEB NEW CONNECTION', 'PASSPORT', 'PROVIDENT FUND', 'TRAFFIC POLICE FINE', 'VOTER ID', 'UDYOG AADHAR', 'UNORGANIZED WORKERS', 'VEHICLE TAX', 'TNEB', 'OBC CERTIFICATE', 'TYPING']})

def formSubmit(request):
    customer_details_mandatory = ['name', 'phone', 'aadhar', 'email', 'job_date', 'total_amount', 'advance_amount', 'job_explain_1', 'job_explain_2', 'job_submitted_by']
    my_uploaded_file = request.FILES.getlist('myfiles')
    files_data = {}
    files_ref_id = None
    
    try:
        if my_uploaded_file:
            for  idx, i in enumerate(my_uploaded_file):
                files = i.file.read()
                encoded_string = base64.b64encode(files)
                files_data[str(i)] = str(encoded_string)
            file_doc = db.db.collection('FILES').document()
            file_doc.set(files_data)
            files_ref_id = file_doc.id
        if request.method=="POST":
            jobs = request.POST.getlist('checks')
            details_json = {}
            for i in customer_details_mandatory:
                details_json[i] = request.POST[i]
            details_json["jobs_list"] = jobs
        data = {"status": "pending", 'job_data': details_json, "files_ref": files_ref_id if files_ref_id else None}
        doc_ref = db.db.collection('JOBS').document()
        doc_ref.set(data)
        messages.success(request, {'status': "Success",'detail': 'JOB submitted successfully!'})
    except Exception as e:
        messages.success(request, {'status': "Failed",'detail': 'JOB Failed to submit! Contact Admin!'})
    return redirect('dashboard')


def admin(request):
    page = 1
    status = "pending"
    if request.method == 'GET':
        page = request.GET.get('page')   
        status = request.GET.get('status')
    docs = db.db.collection('JOBS').where('status', '==', 'completed').stream()
    data = []
    for doc in docs:
        temp = doc.to_dict()
        temp["id"] = doc.id
        data.append(temp)    
    return render(request, 'admin.html', {"data": data})