from django.shortcuts import render, redirect
from .forms import ServiceForm  
from django.core.mail import EmailMessage  # Import EmailMessage
from django.conf import settings
from django.contrib import messages  

def service(request):
    form = ServiceForm()
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name  = form.cleaned_data['last_name']
            email      = form.cleaned_data['email']
            service    = form.cleaned_data['service']  
            file       = form.cleaned_data['file']
            
            print(form.cleaned_data, request.FILES)
            
            subject = 'New Service Request'
            message = f'''
            You have received a new service request:

            Name: {first_name} {last_name}
            Client Email: {email}
            Service: {service}
            File: {file.name if file else "No file uploaded"}
            '''
            recipient_list = [settings.DEFAULT_FROM_EMAIL] 

            try:
                email_message = EmailMessage(
                    subject=subject,
                    body=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=recipient_list
                )
                
                if file:
                    email_message.attach(file.name, file.read(), file.content_type)

                email_message.send()
                return redirect('services:success')  

            except Exception as e:
                messages.error(request, f'Error sending email: {str(e)}')  

    return render(request, 'services/service.html', {'form': form})



def success(request):
    return render(request, 'services/success.html')