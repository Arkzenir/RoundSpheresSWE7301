from django.shortcuts import render, redirect
from django.http import HttpResponse 
from .models import membershipModel



def home(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    data = request.GET
    message = data.get('message', '') 
    return render(request, "register.html", { "message": message })

def adminrecords(request):
    data = request.GET
    message = data.get('message', '')
    records= membershipModel.objects.all()
    return render(request, "adminrecords.html", {"records": records, "message": message })

def adminprofile(request):
    try:
        data = request.GET
        id = data['id']
        record= membershipModel.objects.get(id=id)
        return render(request, "adminprofile.html", {"profile": record })
    
    except:
        message = "record no longer exist for the selected id"
        return redirect('/adminrecords/?message=' + message)
    
def adminupdate(request):
    data = request.GET
    id = data['id']
    message = data.get('message', '')
    record= membershipModel.objects.get(id=id)
    return render(request, 'adminupdate.html', {"profile": record, "message": message })  

def adminimg(request):
    data = request.GET
    id = data['id']
    message = data.get('message', '')
    return render(request, "adminprofileIMG.html", {"id": id, "message": message } )  


def delete(request):

    try:
        data = request.GET
        id = data['id']
        message = "Record has been deleted successfully"
        record= membershipModel.objects.get(id=id)
        record.delete()
        return redirect('/adminrecords/?message=' + message)

    except:
        message = "Record can not be deleted presently, please try again"
        return redirect('/adminrecords/?message=' + message)

# Create your views here.
