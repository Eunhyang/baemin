from django.shortcuts import render

# Create your views here.
def index(request):
    # article_list = Article.objects.all()
    # ctx = {
    #     "article_list" : article_list
    # }
    return render(request, 'index.html', {})
