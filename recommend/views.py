from django.http import HttpResponse
from recommend.models import Popular_Movie
from recommend.movie import utils
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
