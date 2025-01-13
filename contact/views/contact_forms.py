from django.shortcuts import render, get_object_or_404,redirect
from django.core.paginator import Paginator
from django.db.models import Q
from contact.models import Contact
from django.http import Http404
from contact.forms import ContactForm
from contact.models import Contact


def create(request):
  if request.method == 'POST':
    form = ContactForm(request.POST)

    context ={
      'form': form
    }

    if form.is_valid():
      form.save()
      return redirect('contact:create')


    return render(
        request,
        'contact/create.html',
        context
    ) 
  
  context ={
    'form': ContactForm()
  }
  return render(
      request,
      'contact/create.html',
      context
  ) 
