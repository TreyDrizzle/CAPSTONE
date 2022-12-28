from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_request, get_dealers_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)
# ...


# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)
# Create a `login_request` view to handle sign in request
# def login_request(request):
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        
    

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request

def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)

            return redirect('djangoapp:index')
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/CD0201-xxx-nodesample123_Tyler/dealership-package/get-dealerships"
        dealerships = get_dealers_from_cf(url)
        context["dealership_list"] = dealerships
        return render(request, 'djangoapp/index.html', context)
# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealername, id):
    context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/CD0201-xxx-nodesample123_Tyler/dealership-package/get-dealerships"
        context2={}
        reviews = get_dealer_reviews_from_cf(url, id)
        review_all = ' '.join([review_list.review for review_list in reviews])
        context = reviews
        context2["list"]=context
        context2["dealername"]=dealername
        context2["id"]=id
        return render(request, 'djangoapp/dealer_details.html', context2)
          

# Create a `add_review` view to submit a review


def add_review(request, id, dealername):
    context = {}
    user = request.user
    if user.is_authenticated:
        if request.method == "POST":
            #@requires_csrf_token
            #json_payload = {}
            #json_payload["review"] = request.POST['review']
            #json_payload["purchase"] = request.POST.get('purchase')
            #json_payload["car"] = request.POST.get('car')
            #json_payload["purchasedate"] = request.POST.get('purchasedate')
            
            username = request.user.username
            print(request.POST)
            payload = dict()
            car_id = request.POST["car"]
            car = CarModel.car_manager.get(pk=car_id)
            payload["time"] = datetime.utcnow().isoformat()
            payload["name"] = username
            payload["dealership"] = id
            payload["id"] = id
            payload["review"] = request.POST["content"]
            payload["purchase"] = False
            if "purchasecheck" in request.POST:
                if request.POST["purchasecheck"] == 'on':
                    payload["purchase"] = True
            payload["purchase_date"] = request.POST["purchasedate"]
            payload["car_make"] = car.make.name
            payload["car_model"] = car.name
            payload["car_year"] = int(car.year)

            new_payload = {}
            new_payload["review"] = payload
            
            url = "https://us-south.functions.appdomain.cloud/api/v1/web/CD0201-xxx-nodesample123_Tyler/dealership-package/get-dealerships"
            post_request(url, new_payload)
            return redirect('djangoapp:dealer_details', **{"dealername":dealername, "id":id})
            
            #url = "https://3dbc2a14.us-south.apigw.appdomain.cloud/postreview/api/review"
            #result = post_request(url, json_payload)
            #return HttpResponse(json_payload)
        
        elif request.method == "GET":
            models = list(CarModel.car_manager.all().filter(dealerid=id))
            context["cars"] = models
            context["id"] = id
            #dealer = list(CarDealer.dealer_manager.all().filter(id=id))
            context["dealer"] = dealername
            return render(request, 'djangoapp/add_review.html', context)

