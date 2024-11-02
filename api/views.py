from django.shortcuts import render
from . import views
from .models import *
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import psutil
# Create your views here.
def upload(request):
    # Get disk space information
    disk_info = psutil.disk_usage('/')

    # Convert bytes to gigabytes for easier readability
    total_space_gb = round(disk_info.total / (1024 ** 3), 2)
    used_space_gb = round(disk_info.used / (1024 ** 3), 2)
    free_space_gb = round(disk_info.free / (1024 ** 3), 2)

    context = {
        'total_space': total_space_gb,
        'used_space': used_space_gb,
        'free_space': free_space_gb,
    }

    if request.method == 'POST':
        files = request.FILES.getlist('files')
        for file in files:
            file_obj = File(file=file)
            file_obj.save()

    return render(request, 'api/upload.html', context)

def list(request):
    files = File.objects.all()
    content =""
   
    for file_obj in files:
        link = f"https://autop-6gjh.onrender.com/download/{file_obj.id}\n"
        content+=link
        

    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'inline; filename=links.txt'
    return response 

def download(request, id):
    file = get_object_or_404(File, pk=id)
    response = FileResponse(file.file, as_attachment=True)
    
    
    file.delete()
    return response
