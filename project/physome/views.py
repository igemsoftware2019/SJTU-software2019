from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader,RequestContext

app_name = 'physome'
# Create your views here.
def index(request):
	#return HttpResponse('hello,world.')
	# loader.get_template('app1/index.html')
	# context = RequestContext(request,{})
	# res_html = temp.render(context)
	# return HttpResponse(res_html)
	#或者封装起来
	return render(request,'physome/index.html')

def partdata(request):
	return render(request,'physome/partdata.html')

def metadata(request):
	return render(request,'physome/metadata.html')

def prediction(request):
	return render(request,'physome/prediction.html')

def help(request):
	return render(request,'physome/help.html')