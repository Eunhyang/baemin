from django.contrib.auth import (
    authenticate,
    login as auth_login,
    logout as auth_logout
    )
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect

from client.views import common_login, common_signup
from client.models import Ordertime
from .forms import PartnerForm, MenuForm
from .models import Menu

URL_LOGIN = "/partner/login/"

def patner_group_check(user):
    return "partner" in [group.name for group in user.groups.all()]
# Create your views here.
@user_passes_test(patner_group_check, login_url = URL_LOGIN)
@login_required(login_url = URL_LOGIN)
def index(request):
    ctx = {}
    if request.method == "GET":
        # Partnerform 객체 생성
        partner_form = PartnerForm()
        # 태워보냄
        ctx.update({"partner_form":partner_form})
    elif request.method == "POST":
        partner_form = PartnerForm(request.POST)
        if partner_form.is_valid():
            partner = partner_form.save(commit = False)
            partner.user = request.user
            partner.save()
            return redirect("/partner/")
        else:
            ctx.update({"partner_form":partner_form})

    return render(request, "index.html", ctx)

def login(request):
    ctx = { "is_client" : False }
    return common_login(request, ctx, "partner")


def logout(request):
    auth_logout(request)
    return redirect("/")

def signup(request):
    ctx = {}
    return common_signup(request, ctx, "partner")

@user_passes_test(patner_group_check, login_url = URL_LOGIN)
@login_required(login_url = URL_LOGIN)
def edit_info(request):
    ctx = {}
    if request.method == "GET":
        # Partnerform 객체 생성
        partner_form = PartnerForm(instance=request.user.partner)
        # 태워보냄
        ctx.update({"partner_form":partner_form})
    elif request.method == "POST":
        partner_form = PartnerForm(
            request.POST,
            instance=request.user.partner
            )
        if partner_form.is_valid():
            partner = partner_form.save(commit = False)
            partner.user = request.user
            partner.save()
            return redirect("/partner/")
        else:
            ctx.update({"partner_form":partner_form})

    return render(request, "edit_info.html", ctx)

# def edit_info(request):
#     ctx = {}
#     if request.method == "GET":
#         # Partnerform 객체 생성
#         partner = request.user.partner
#         # 태워보냄
#         ctx.update({"partner":partner})
#     elif request.method == "POST":
#         partner = request.user.partner
#         partner.name = request.POST.get('name')
#         partner.contact = request.POST.get('contact')
#         partner.address = request.POST.get('address')
#         partner.save()
#         return redirect("/partner/")
#     return render(request, "edit_info.html", ctx)
@user_passes_test(patner_group_check, login_url = URL_LOGIN)
@login_required(login_url = URL_LOGIN)
def menu(request):
    ctx = {}
    menu_list = Menu.objects.filter(partner=request.user.partner)
    # 태워보냄
    ctx.update({"menu_list":menu_list})
    return render(request, "menu_list.html", ctx)

@user_passes_test(patner_group_check, login_url = URL_LOGIN)
@login_required(login_url = URL_LOGIN)
def menu_add(request):
    ctx = {}
    if request.method == "GET":
        # Partnerform 객체 생성
        menu_form = MenuForm()
        # 태워보냄
        ctx.update({"menu_form":menu_form})
    elif request.method == "POST":
        print('----------------Post성공----------------')
        menu_form = MenuForm(request.POST,request.FILES)
        if menu_form.is_valid():
            print('----------------메뉴 체크----------------')
            menu = menu_form.save(commit = False)
            menu.partner = request.user.partner
            menu.save()
            print('----------------메뉴 등록 성공----------------')
            return redirect("/partner/menu/")
        else:
            print('----------------메뉴 등록 실패----------------')
            ctx.update({"menu_form":menu_form})

    return render(request, "menu_add.html", ctx)

@user_passes_test(patner_group_check, login_url = URL_LOGIN)
@login_required(login_url = URL_LOGIN)
def menu_detail(requst,menu_id):
    ctx = {}
    menu = Menu.objects.get(id = menu_id)
    # 태워보냄
    ctx.update({"menu":menu})
    return render(requst, "menu_detail.html", ctx)

@user_passes_test(patner_group_check, login_url = URL_LOGIN)
@login_required(login_url = URL_LOGIN)
def menu_edit(request, menu_id):
    ctx = {}
    menu = Menu.objects.get(id = menu_id)
    if request.method == "GET":
        # Partnerform 객체 생성
        menu_form = MenuForm(instance = menu)
        # 태워보냄
        ctx.update({"menu_form":menu_form})
    elif request.method == "POST":
        menu_form = MenuForm(request.POST,instance=menu)
        if menu_form.is_valid():
            menu = menu_form.save(commit = False)
            menu.partner = request.user.partner
            menu.save()
            return redirect("/partner/menu/" + menu_id)
        else:
            ctx.update({"menu_form":menu_form})

    return render(request, "menu_add.html", ctx)

@user_passes_test(patner_group_check, login_url = URL_LOGIN)
@login_required(login_url = URL_LOGIN)
def menu_delete(request, menu_id):
    menu = Menu.objects.get(id = menu_id)
    menu.delete()
    return redirect("/partner/menu/")

@user_passes_test(patner_group_check, login_url = URL_LOGIN)
@login_required(login_url = URL_LOGIN)
def order(request):
    ctx = {}
    item_list = []
    partner = request.user.partner
    menu_list = Menu.objects.filter(partner=partner)
    for menu in menu_list:
        item_list.extend([
        item for item in Ordertime.objects.filter(menu=menu)
        ])
    #왜 집합으로 두는가? 집합:중복허용x순서없음
    order_set = set([item.order for item in item_list])
    ctx.update({
    "order_set" : order_set,
    "item_list" : item_list,
    })
    return render(request, "order_list_for_partner.html", ctx)
