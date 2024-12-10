from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import membershipModel
from django.core.files.storage import default_storage
from django.contrib.auth.hashers import make_password, check_password
import random

def registration(request):
    try:
        if request.method == "POST":
            form = request.POST
            saveData = membershipModel.objects.create(
            First_name = form['First_name'],
            Last_name = form['Last_name'],
            User_name = form['User_name'],
            Email_address = form['Email_address'],
            Password = make_password(form['Password']),
            )
            message = "Success"
            return redirect('/../register', {"message": message })
            
        else:
            message = "INVALID request"
            return render(request, "register.html", {"message": message })
    except Exception as error:
        message = "something went wrong, please try again. Error: "
        print(error)
        return render(request, "register.html", {"message": message })

def updaterecord(request):
    try:
        id = 0
        if request.method == "POST":
            form = request.POST
            id = form['id']
            record = membershipModel.objects.get(id=id)
            record.First_name = form['First_name']
            record.Last_name = form['Last_name']
            record.User_name = form['User_name']
            record.Email_address = form['Email_address']
            record.Password =  make_password(form['Password']),
            record.save()
            message = "profile updated successfully"
            return redirect('/adminrecords/?id=' + str(id) + '&message=' + message)

        else:
            message = "INVALID request"
            return redirect('/adminupdate/?message=' + message)
    except Exception as error:
        message = "something went wrong, please try again. Error: "+str(error)
        return redirect('/adminupdate/?message=' + message)

def uploadproductimg(request):
    try:
        if request.method == "POST":
            uploadedfile = request.FILES["image_url"]
            form = request.POST
            id = form['id']
            # print(uploadedfile)
            location= "user/"
            getextension = uploadedfile.name.split('.')
            randomname = str(random.randint(1, 999999999999))
            filename = randomname+"."+getextension[1]
            default_storage.save(location+filename, uploadedfile)
            getlocation = default_storage.url(location+filename)
            record = membershipModel.objects.get(id=id)
            record.image_url = getlocation
            record.save()
            message = "success "
            return render(request, "adminprofile.html", {"message": message })


    except Exception as error:
        message = "something went wrong, please try again. Error: "+str(error)
        return redirect('/adminimg/?id=' + str(id) + '&message=' + message)