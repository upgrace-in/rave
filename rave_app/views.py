from django.core import exceptions
from django.db.models.fields import CommaSeparatedIntegerField
from django.http.response import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators import csrf
from . import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.models import User
import requests
from rave_app import models
import schedule
import threading
import time
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json


def index(rst):
    data = models.nfts.objects.filter(approved=True, purchased=False)
    return render(rst, 'index.html', {'data': data})

# APIs


@csrf_exempt
def verify_price(rst, id):
    data = models.nfts.objects.get(id=id)
    if data.price == float(rst.POST['price']):
        return JsonResponse(json.dumps({'price': data.price, 'wallet_address': data.wallet_address}), safe=False)
    else:
        raise Http404

@csrf_exempt
def update_txhash(rst, id):
    try:
        mdl = models.nfts.objects.get(id=id)
        mdl.transaction_id = rst.POST['txhash']
        mdl.applied_for_purchasing = True
        mdl.buyer_id = rst.POST['buyer_id']
        mdl.save()
        return HttpResponse("Success")
    except EOFError as e:
        print(e)
        raise Http404

def applied_for_purchasing(self):
    mdl = models.nfts.objects.filter(applied_for_purchasing=True)
    data = serializers.serialize('json', mdl)
    return JsonResponse(data, safe=False)


def purchased(rst, id):
    try:
        mdl = models.nfts.objects.get(id=id)
        mdl.purchased = True
        mdl.applied_for_purchasing = False
        mdl.approved = False
        mdl.save()
        return HttpResponse("Success")
    except EOFError as e:
        return HttpResponse("Error", e)


# APIs


def nft_status(rst, id):
    nft = models.nfts.objects.get(id=id)
    if nft.approved == True:
        nft.approved = False
    else:
        nft.approved = True
    nft.save()
    return redirect('admin_panel')


def admin_panel(rst):
    users = User.objects.all()
    nfts = models.nfts.objects.all()
    data = {
        'users_count': users.count,
        'users': users,
        'nfts': nfts
    }
    return render(rst, 'admin.html', data)


def view_nft(rst, id):
    try:
        data = models.nfts.objects.get(id=id)
        return render(rst, 'view_nft.html', {'data': data})
    except EOFError:
        return Http404


def dashboard(rst):
    own_nfts = models.nfts.objects.filter(seller_id=rst.user, purchased=False)
    bought_nfts = models.nfts.objects.filter(buyer_id=rst.user.email, purchased=True)
    data = {
        'own_nfts': own_nfts,
        'bought_nfts': bought_nfts
    }
    return render(rst, 'dashboard.html', data)


def marketplace(rst):
    data = models.nfts.objects.filter(approved=True)
    return render(rst, 'marketplace.html', {'data': data})


def create_nft(rst):
    if rst.method == 'POST':
        try:
            m = models.nfts.objects.create(
                file=rst.FILES['file'],
                seller_id=rst.user,
                wallet_address=rst.POST['wallet_address'],
                title=rst.POST['title'],
                desc=rst.POST['desc'],
                price=rst.POST['price']
                
            )
            m.save()
            return redirect('dashboard')
        except EOFError as e:
            return Http404
    else:
        return render(rst, 'create_nft.html')


def user_func(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        username = email.split('@')
        try:
            u = User.objects.get(email=email)
            if u:
                user = authenticate(
                    request, username=u.username, email=email, password=password)
                if user:
                    login(request, user)
                    return redirect('index')
                else:
                    e = "Please Check Your Credentials"
                    return render(request, 'login.html', {'e': e})
        except ObjectDoesNotExist:
            user = User.objects.create_user(
                username=username[0], email=email, password=password)
            user.save()
            login(request, user)
            return redirect('index')
    else:
        return HttpResponse("Method Not Allowed!")


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('index')
