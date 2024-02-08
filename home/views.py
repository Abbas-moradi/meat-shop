from django.shortcuts import render
from django.views import View

class Home(View):
    home_temp = 'index.html'
    def get(self, request):
        temp = self.home_temp
        return render(request, temp)
    
    def post(self, request):
        pass