from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import os
import pymongo
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import requests
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from .forms import UserForm
import bcrypt
from .forms import LoginForm
from .forms import UserProfileForm
import json
from dotenv import load_dotenv


def getuserinfo(request):
    load_dotenv()
    uri = os.getenv("MONGODB_URL")
    client = MongoClient(uri)
    username = "mmills6060" 
    db = client['myDatabase']
    user_collection = db['users']
    user = user_collection.find_one({'username': username})
    if not user:
        print("Please login first.")
    else:
        if user['username'] == username:
                first_name = user.get('first_name')
                last_name = user.get('last_name')
                phone_number = user.get('phone_number')
                email = user.get('email')

                devices = user.get('devices', [])
                number_of_files = user.get('number_of_files', [])
                number_of_devices = user.get('number_of_devices', [])
                overall_date_added = user.get('overall_date_added', [])
                total_average_upload_speed = user.get('total_average_upload_speed', [])
                total_average_download_speed = user.get('total_average_download_speed', [])
                total_device_storage = user.get('total_device_storage', [])
 
                user_data = {
                        "first_name": first_name,
                        "last_name": last_name,
                        "phone_number": phone_number,
                        "email": email,
                        "devices": devices,
                        "number_of_devices": number_of_devices,
                        "number_of_files": number_of_files,
                        "overall_date_added": overall_date_added,
                        "total_average_upload_speed": total_average_upload_speed,
                        "total_average_download_speed": total_average_download_speed,
                        "total_device_storage": total_device_storage,
                        }
                return JsonResponse(user_data)

def getuserinfo2(request, username):
    load_dotenv()
    uri = os.getenv("MONGODB_URL")
    client = MongoClient(uri)
    username = username 
    db = client['myDatabase']
    user_collection = db['users']
    user = user_collection.find_one({'username': username})
    if not user:
        print("Please login first.")
    else:
        if user['username'] == username:
                first_name = user.get('first_name')
                last_name = user.get('last_name')
                phone_number = user.get('phone_number')
                email = user.get('email')

                devices = user.get('devices', [])
                number_of_files = user.get('number_of_files', [])
                number_of_devices = user.get('number_of_devices', [])
                overall_date_added = user.get('overall_date_added', [])
                total_average_upload_speed = user.get('total_average_upload_speed', [])
                total_average_download_speed = user.get('total_average_download_speed', [])
                total_device_storage = user.get('total_device_storage', [])
 
                user_data = {
                        "first_name": first_name,
                        "last_name": last_name,
                        "phone_number": phone_number,
                        "email": email,
                        "devices": devices,
                        "number_of_devices": number_of_devices,
                        "number_of_files": number_of_files,
                        "overall_date_added": overall_date_added,
                        "total_average_upload_speed": total_average_upload_speed,
                        "total_average_download_speed": total_average_download_speed,
                        "total_device_storage": total_device_storage,
                        }
                return JsonResponse(user_data)





def homepage(request):
    service = os.environ.get('K_SERVICE', 'Unknown service')
    revision = os.environ.get('K_REVISION', 'Unknown revision')
    
    return render(request, 'homepage.html', context={
        "message": "It's running!",
        "Service": service,
        "Revision": revision,
    })

def aboutpage(request):
    return render(request, 'aboutpage.html', context={})


def download_debian_package(request):
    file_path = os.path.join(settings.BASE_DIR, 'helloapp/templates/bcloud_1.0.0_all.deb')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.debian.binary-package")
            response['Content-Disposition'] = 'attachment; filename="bcloud_1.0.0.0_all.deb"'
            return response
    else:
        response = HttpResponse("File not found.", status=404)
    return response


def addusernopassword(request):
    # MongoDB connection string
    load_dotenv()
    uri = os.getenv("MONGODB_URL")
 
    # Create a MongoDB client
    client = pymongo.MongoClient(uri, server_api=ServerApi('1'))

    # Select the database and collection
    db = client['myDatabase']
    user_collection = db['users']

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            # Insert the user into the database
            try:
                user_collection.insert_one({"username": username})
                message = f"User '{username}' added successfully."
            except pymongo.errors.OperationFailure as e:
                message = f"An error occurred: {e}"
            return render(request, 'user_added.html', {'message': message})
    else:
        form = UserForm()

    return render(request, 'add_user.html', {'form': form})
def adduser1(request):
    load_dotenv()
    uri = os.getenv("MONGODB_URL")
 
    client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
    db = client['myDatabase']
    user_collection = db['users']

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['first_name']
            username = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']  # Get the password from the form

            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            try:
                # Insert the user with the hashed password into the database
                user_collection.insert_one({"username": username, "password": hashed_password})
                message = f"User '{username}' added successfully."
            except pymongo.errors.OperationFailure as e:
                message = f"An error occurred: {e}"
            return render(request, 'user_added.html', {'message': message})
    else:
        form = UserForm()

    return render(request, 'add_user.html', {'form': form})

def adduser(request):
    load_dotenv()
    uri = os.getenv("MONGODB_URL")
 
    client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
    db = client['myDatabase']
    user_collection = db['users']


    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            firstName = form.cleaned_data['first_name']
            lastName = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password'].encode('utf-8')

            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

            # Create a new user document with additional fields set to null
            new_user = {
                "username": username,
                "password": hashed_password,
                "first_name": firstName,
                "last_name": lastName,
                "phone_number": None,
                "email": None,
                "devices": [],
                "files": []
            }

            try:
                user_collection.insert_one(new_user)
                message = f"User '{username}' added successfully."
            except pymongo.errors.OperationFailure as e:
                message = f"An error occurred: {e}"

            return render(request, 'user_added.html', {'message': message})

    else:
        form = UserForm()

    return render(request, 'add_user.html', {'form': form})


def login(request):
    load_dotenv()
    uri = os.getenv("MONGODB_URL")
 


    client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
    db = client['myDatabase']
    user_collection = db['users']

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password'].encode('utf-8')

            user = user_collection.find_one({'username': username})

            if user and bcrypt.checkpw(password, user['password']):
                return redirect('dashboard', username=username)  # Redirect to a home page or dashboard
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})



@csrf_exempt  # Disable CSRF token for this view only if necessary (e.g., for external API access)
@require_http_methods(["POST"])
def login_api(request):

    load_dotenv()
    uri = os.getenv("MONGODB_URL")
 

    client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
    db = client['myDatabase']
    user_collection = db['users']

    # Ensure the request body is JSON
    try:
        data = json.loads(request.body)

        # extract username and password from the JSON data
        username = data.get('username')
        password = data.get('password').encode('utf-8')

        user = user_collection.find_one({'username': username})

        if user and bcrypt.checkpw(password, user['password']):
            return JsonResponse({'response': 'success'})
        else:
            return JsonResponse({'response': 'fail'})


    except ValueError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

@csrf_exempt  # Disable CSRF token for this view only if necessary (e.g., for external API access)
@require_http_methods(["POST"])
def registration_api(request):

    load_dotenv()
    uri = os.getenv("MONGODB_URL")
 

    client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
    db = client['myDatabase']
    user_collection = db['users']

    # Ensure the request body is JSON
    try:
        data = json.loads(request.body)

        # extract username and password from the JSON data
        firstName = data.get('firstName')
        lastName = data.get('last1Name')
        username = data.get('username')
        password = data.get('password').encode('utf-8')


        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        # Create a new user document with additional fields set to null
        new_user = {
            "username": username,
            "password": hashed_password,
            "first_name": firstName,
            "last_name": lastName,
            "phone_number": None,
            "email": None,
            "devices": [],
            "number_of_devices": [],
            "number_of_files": [],
            "overall_date_added": [],
            "total_average_download_speed": [],
            "total_average_upload_speed": [],
            "total_device_storage": [],
            "total_average_cpu_usage": [],
            "total_average_gpu_usage": [],
            "total_average_ram_usage": [],
        }

        try:
            user_collection.insert_one(new_user)
            message = f"User '{username}' added successfully."
            return JsonResponse({'response': 'success'})

        except pymongo.errors.OperationFailure as e:
            message = f"An error occurred: {e}"
            return JsonResponse({'response': 'fail'})
    except ValueError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)






def dashboard(request, username):
    # Render the dashboard template with the username

    load_dotenv()
    uri = os.getenv("MONGODB_URL")
 

    client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
    db = client['myDatabase']
    user_collection = db['users']

    user = user_collection.find_one({'username': username})
    first_name = user.get('first_name', 'User')  # Default to 'User' if first name is not set
    files = user.get('files', 'files')  # Default to 'User' if first name is not set
    devices = user.get('devices', 'devices')  # Default to 'User' if first name is not set
    return render(request, 'dashboard.html', {'username': username, 'first_name': first_name, 'files': files, 'devices': devices})

def update_user_profile(request, username):

    load_dotenv()
    uri = os.getenv("MONGODB_URL")

    client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
    db = client['myDatabase']
    user_collection = db['users']

    user = user_collection.find_one({'username': username})

    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user_collection.update_one(
                {'username': username},
                {'$set': {
                    'first_name': form.cleaned_data['first_name'] or user['first_name'],
                    'last_name': form.cleaned_data['last_name'] or user['last_name'],
                    'phone_number': form.cleaned_data['phone_number'] or user['phone_number'],
                    'email': form.cleaned_data['email'] or user['email']
                }}
            )
            return redirect('dashboard', username=username)
    else:
        form = UserProfileForm(initial=user)

    return render(request, 'update_profile.html', {'form': form, 'username': username})



