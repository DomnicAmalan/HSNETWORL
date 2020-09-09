from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import Context, loader
import base64
from .helpers import db
import json
from django.contrib import messages
from .constants import options, request_params
from datetime import date

# Create your views here.
def signin(request):
    return render(request, 'signin.html', {'poll': "p"})

def phoneAuth(request):
    return render(request, 'phoneauth.html')

def dashboard(request, data=None, id=None):  
    return render(request, 'Dashboard.html', {"options": options, "data": data, "id":id, "submit_url": '/customer-service/submit/edit/' + id if id else '/customer-service/submit' })

def formSubmit(request):
    customer_details_mandatory = request_params
    my_uploaded_file = request.FILES.getlist('myfiles')
    files_data = {}
    files_ref_id = None
    try:
        files_ref_list = []
        if my_uploaded_file:
            for  idx, i in enumerate(my_uploaded_file):
                files = i.file.read()
                encoded_string = base64.b64encode(files)
                files_data = {"name": str(i), "file": encoded_string}
                file_doc = db.db.collection('FILES').document()
                file_doc.set(files_data)
                files_ref_list.append({"name": str(i), "file": file_doc.id})
        if request.method=="POST":
            jobs = request.POST.getlist('checks')
            details_json = {}
            today = date.today()

            job_date = today.strftime("%d/%m/%Y")
            details_json["job_date"] = job_date
            for i in customer_details_mandatory:
                details_json[i] = request.POST[i]
            details_json["jobs_list"] = jobs
        data = {"status": "pending", 'job_data': details_json, "files_ref": files_ref_list if files_ref_list else []}
        doc_ref = db.db.collection('JOBS').document()
        doc_ref.set(data)
        messages.success(request, json.dumps({'status': True,'detail': 'JOB submitted successfully!'}))
    except Exception as e:  
        messages.success(request, json.dumps({'status': False,'detail': 'JOB Failed to submit! Contact Admin!'}))
    return redirect('dashboard')

def editSubmit(request, job_id):
    status = 'pending'
    reference_number = ''
    my_uploaded_file = request.FILES.getlist('myfiles')
    files_ref_list = []

    try:
        status = request.POST['status']
        reference_number = request.POST['reference_number']
    except:
        status = 'pending'
    
    customer_details_mandatory = request_params
    if not status == 'completed':
        if my_uploaded_file:
            for  idx, i in enumerate(my_uploaded_file):
                files = i.file.read()
                encoded_string = base64.b64encode(files)
                files_data = {"name": str(i), "file": encoded_string}
                file_doc = db.db.collection('FILES').document()
                file_doc.set(files_data)
                files_ref_list.append({"name": str(i), "file": file_doc.id})
        data = db.db.collection('JOBS').document(job_id).get().to_dict()
        files_ref_list = data["files_ref"] + files_ref_list
    else:
        data = db.db.collection('JOBS').document(job_id).get().to_dict()
        for i in data["files_ref"]:
            db.db.collection('JOBS').document(i).delete()
    if request.method=="POST":
            jobs = request.POST.getlist('checks')
            details_json = {}
            today = date.today()
            job_date = today.strftime("%d/%m/%Y")
            details_json["job_date"] = job_date
            for i in customer_details_mandatory:
                details_json[i] = request.POST[i]
            details_json["jobs_list"] = jobs
            details_json['reference_number'] = reference_number
            data = {"status": status, 'job_data': details_json, "files_ref": files_ref_list if files_ref_list else []}
            db.db.collection('JOBS').document(job_id).set(data)
    return redirect('admin')

def admin(request):
    try:
        status = request.GET['status']
    except:
        status = 'pending'
    search = request.GET.get('search')
    docs = db.db.collection('JOBS').where('status', '==', status).stream()
    data = []
    for doc in docs:
        temp = doc.to_dict()
        temp["id"] = doc.id
        temp["delete_url"] = '/customer-service/deletejob/' + temp["id"]
        temp["edit_url"] = '/customer-service/editjob/' + temp["id"]
        data.append(temp)    
    return render(request, 'admin.html', {"data": data, "status": status})

def deleteJob(request, job_id=None):
    file_data = db.db.collection('JOBS').documents(job_id).get()

    db.db.collection('JOBS').document(job_id).delete()
    return redirect('admin')

def editjob(request, job_id=None):
    data = db.db.collection('JOBS').document(job_id).get()
    return dashboard(request, data=data.to_dict(), id=job_id)

def ViewFile(request, file_id):
    data = db.db.collection('FILES').document(file_id).get().to_dict()
    data = data["file"].decode('utf-8')
    return render(request, 'preview.html', {"file": data})

def DeleteFile(request, file_id, job_id):
    data = db.db.collection('FILES').document(file_id).delete()
    data = db.db.collection('JOBS').document(job_id).get().to_dict()
    return redirect('admin')