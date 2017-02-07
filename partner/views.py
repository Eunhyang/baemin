from django.contrib.auth import (
    authenticate,
    login as auth_login,
    logout as auth_logout
    )
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import PartnerForm, MenuForm
from .models import Menu

# Create your views here.
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
    ctx = {}

    if request.method == "GET":
        pass
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            print('----------------로그인 성공----------------')
            auth_login(request, user)
            return redirect("/partner/")
        else:
            print('----------------사용자 없음----------------')
            ctx.update({"error" : "사용자가 없습니다."})

    return render(request, "login.html", ctx)

def logout(request):
    auth_logout(request)
    return redirect("/partner/")

def signup(request):
    if request.method == "GET":
        pass
    elif request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        # print(username, email, password)

        user = User.objects.create_user(username, email, password)
        # Article.objects.create(title="", content="")

    ctx = {}
    return render(request, "signup.html", ctx)

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

def menu(request):
    ctx = {}
    menu_list = Menu.objects.filter(partner=request.user.partner)
    # 태워보냄
    ctx.update({"menu_list":menu_list})
    return render(request, "menu_list.html", ctx)

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

def menu_detail(requst,menu_id):
    ctx = {}
    menu = Menu.objects.get(id = menu_id)
    # 태워보냄
    ctx.update({"menu":menu})
    return render(requst, "menu_detail.html", ctx)

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

def menu_delete(request, menu_id):
    menu = Menu.objects.get(id = menu_id)
    menu.delete()
    return redirect("/partner/menu/")
