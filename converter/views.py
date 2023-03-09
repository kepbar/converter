from django.shortcuts import render, redirect

def base_view(request):
    return redirect('/exchange/welcome')