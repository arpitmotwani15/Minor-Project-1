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
    ids,titles= utils.build_chart("Fantasy")
    ans='<table>'
    for i in range(10):
        ans+='<tr>'
        ans+="<td>"+str(ids[i])+"</td><td>"+titles[i]+"</td>"
        ans+="</tr>"
    ans+="</table>"
    return HttpResponse(ans)

def personalised(request):
    userId=request.GET["uid"]
    title=request.GET["title"]
    titles,ids=utils.hybrid(int(userId),title)
    ans='<table>'
    for i in range(10):
        ans+='<tr>'
        ans+="<td>"+str(ids[i])+"</td><td>"+titles[i]+"</td>"
        ans+="</tr>"
    ans+="</table>"
    return HttpResponse(ans)


