from django.shortcuts import render
from partner.models import Partner
# Create your views here.
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
