from django.shortcuts import render, redirect

def index(request):
    if request.user.username:
        return redirect('subjects:subject-list')
    
    else:
        return render(request, 'index.html')