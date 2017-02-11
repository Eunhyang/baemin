from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import (
    authenticate,
    login as auth_login,
    logout as auth_logout
    )
from django.shortcuts import render, redirect

from partner.models import Partner, Menu
from .models import Client, Order, Ordertime
# Create your views here.
URL_PARTNER = "/partner/"

def client_group_check(user):
    return "client" in [group.name for group in user.groups.all()]

def common_login(request, ctx, group) :
    if request.method == "GET":
        pass

    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            print('----------------로그인 성공----------------')
            if group not in [group.name for group in user.groups.all()]:
                ctx.update({"error":"접근 권한이 없습니다."})
            else:
                auth_login(request, user)
                next_url = request.GET.get(next)
                if next_url:
                    return redirect(next_url)
                else:
                    if group == "client":
                        return redirect("/")
                    else:
                        return redirect("/partner")
        else:
            print('----------------사용자 없음----------------')
            ctx.update({"error" : "사용자가 없습니다."})

    return render(request, "login.html", ctx)

def common_signup(request, ctx, group):
    if request.method == "GET":
        pass
    elif request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        # print(username, email, password)

        user = User.objects.create_user(username, email, password)
        target_group = Group.objects.get(name=group)
        user.groups.add(target_group)

        if group == "client":
            Client.objects.create(user=user, username=username)
            return redirect("/")
        else:
            return redirect("/partner")
        # Article.objects.create(title="", content="")
    return render(request, "signup.html", ctx)


def login(request):
    ctx = { "is_client" : True }
    return common_login(request, ctx, "client")

def signup(request):
    ctx = { "is_client" : True }
    return common_signup(request, ctx, "client")

@user_passes_test(client_group_check, login_url = URL_PARTNER)
def index(request):
    category = request.GET.get("category")
    print(category)
    if not category:
        partner_list = Partner.objects.all()
    elif category:
        partner_list = Partner.objects.filter(category = category)

    # category_list = set([
    #     (partner.category, partner.get_category_display())
    #     for partner in partner_list
    # ])
    ctx = {
        "partner_list" : partner_list,
        # "category_list" : category_list,
    }
    return render(request, 'main.html', ctx)

@user_passes_test(client_group_check, login_url = URL_PARTNER)
def order(request, partner_id):
    ctx = {}
    partner = Partner.objects.get(id=partner_id)
    menu_list = Menu.objects.filter(partner=partner)
    if request.method == "GET":
        print(partner.name)
        ctx.update({
        "partner":partner,
        "menu_list":menu_list,
        })
    elif request.method == "POST":
        order = Order.objects.create(
            client = request.user.client,
            address = 'test'
            )
        for menu in menu_list:
            menu_count = request.POST.get(str(menu.id))
            menu_count = int(menu_count)
            if menu_count > 0 :
                items = Ordertime.objects.create(
                    order = order,
                    menu = menu,
                    count = menu_count
                )
        return redirect("/")

    return render(request, "order_menu_list.html", ctx)
