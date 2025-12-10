from django.shortcuts import render, redirect

def index(request):
    print(request.user)
    print(request.user.username)
    if request.user.username:
        return redirect('subjects:subjects-list')
    
    else:
        return render(request, 'index.html')