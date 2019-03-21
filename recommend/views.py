from django.http import HttpResponse
from recommend.models import Popular_Movie
from recommend.movie import utils
import pandas


def popular(request):
    popular_movies = Popular_Movie.objects.all()
    ans=""
    for i in popular_movies:
        ans+=i.title+"\t"+i.year+"\n"
    return HttpResponse(ans)

def charts(request):
    title,date= utils.build_chart("Fantasy")
    ans=''
    ans+=''.join(title)+"<br/>"
    return HttpResponse(ans)

def personalised(request):
    userId=request.GET["uid"]
    title=request.GET["title"]
    data=utils.hybrid(int(userId),title)
    ans=''
    ans+="<br/>".join(data)
    return HttpResponse(ans)


