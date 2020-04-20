from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Trail, Pictures, Messages, Comments
from .forms import UploadFileForm
from BikeProj.settings import MEDIA_ROOT, MEDIA_URL
import bcrypt

def login_reg(request):
    return render(request, "login.html")

def login(request):
    errors = User.objects.login_validator(request.POST)
    print("errors")
    print(errors)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
            print("YOU MESSED UP")
        return redirect("/")
    else:
        emails = request.POST["email_input"]
        passwords = request.POST["password_input"]
        get_user = User.objects.get(email=emails)
        valid_pw = bcrypt.checkpw(request.POST["password_input"].encode(), get_user.password.encode())
        request.session["user_id"] = get_user.id
        print("DOPE")
        return redirect("/dashboard")

def register_user(request):
    errors = User.objects.reg_validator(request.POST)
    print("errors")
    print(errors)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
            print("!!!!!ERRORSSSSS!!!!!!")
        return redirect("/login")
    else:
        first_names = request.POST["first_name_input"]
        last_names = request.POST["last_name_input"]
        emails = request.POST["email_input"]
        passwords = request.POST["password_input"]
        confirm_passwords = request.POST["confirm_password_input"]
        rider_levels = request.POST["rider_level"]
        bike_types = request.POST["bike_type"]
        hashpw = bcrypt.hashpw(passwords.encode(), bcrypt.gensalt()).decode() # this line hashes the password
        add_user = User.objects.create(first_name=first_names, last_name=last_names, email=emails, password=hashpw, rider_level=rider_levels, bike_type=bike_types)
        userVal = add_user.id
        request.session["user_id"] = add_user.id
        print('NOICE!!!!!!!!!!!!!!')
        return redirect("/dashboard")

def dashboard(request):
    if "user_id" not in request.session:
        print("You must login")
        return redirect("/login")
    this_user = User.objects.get(id=request.session['user_id'])
    context = {
        "user": this_user,
        "all_messages": Messages.objects.all(),
    }
    return render(request, "dashboard.html", context)

def logout(request):
    request.session.clear()
    return redirect("/")

def gallery(request):
    context = {
        "all_images": Pictures.objects.filter(user=User.objects.get(id=request.session['user_id'])),
        "media_root": MEDIA_ROOT,
        "media_url": MEDIA_URL,
    }
    return render(request, "gallery.html", context)

def upload_pic(request):
    if request.method == 'POST':
        titles = request.POST["pic_title_input"]
        descs = request.POST["pic_desc_input"]
        print("*"*100, request.FILES["file"])
        newpic = Pictures.objects.create(img = request.FILES['file'], title=titles, desc=descs, user=User.objects.get(id=request.session['user_id']))
        print(newpic.img)
        newpic.save()
        # newpic.get()
    return redirect("/gallery")

# def display_pics(request):
#     # if request.method == 'FILE':
#     #     print("&"*100, request.FILES["file"])
#     #     img_display = Pictures.objects.all(img = request.FILES['file'], user=User.objects.get(id=request.session['user_id']))
#     #     print(img_display.img)
#     context = {
#         "all_images": Pictures.objects.filter(user=User.objects.get(id=request.session['user_id'])),
#         "media_root": MEDIA_ROOT,
#         "media_url": MEDIA_URL,
#     }
#     return redirect(request, "/gallery", context)
