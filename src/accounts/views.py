from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import RegisterForm, ProfileForm
from .models import Account, Profile
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
import logging
from .decorators import redirect_if_logged_in
import re




logger = logging.getLogger(__name__)

# Utility function to send emails
def send_verification_email(user, request, subject, template_name):
    current_site = get_current_site(request)
    message = render_to_string(template_name, {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email]
    )
    email.send()

# Sign Up
@redirect_if_logged_in
def user_signUp(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            gender = form.cleaned_data['gender']
            user_name = email.split("@")[0]  # Generate username from email
            user_name = re.sub(r'[^a-zA-Z]', '', user_name)

            password = form.cleaned_data['password']

            # Create the user
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                gender=gender,
                username=user_name,
                password=password
            )
            user.save()
            Profile.objects.create(user=user, bio="", photo="avatar.png")

            # Send activation email
            send_verification_email(user, request, 'Please activate your account', 'accounts/account_verification_email.html')
            messages.success(request, 'We sent a verification email, please check your email.')

            return redirect(reverse('accounts:login') + f'?command=verification&email={email}')
    else:
        form = RegisterForm()
    
    context = {
        'form': form,
    }

    return render(request, 'accounts/register.html', context)

# Login
@redirect_if_logged_in
def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'You are logged in.')
            
            # Redirect to the next page if available
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('accounts:profile', username=user.username)
        else:
            messages.error(request, 'Invalid login! Email or password is invalid.')
            return redirect('accounts:login')

    return render(request, 'accounts/login.html')

# Logout
@login_required(login_url='accounts:login')
def logout(request):
    auth_logout(request)
    messages.success(request, 'You are logged out now.')
    return redirect('accounts:login')

# Activate Account
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist) as e:
        logger.error(f"Activation error: {e}")
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('accounts:login')
    else:
        messages.error(request, 'Invalid activation link or the link has expired.')
        return redirect('accounts:sign_up')

# Forgot Password
def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('accounts:forgotPassword')
    return render(request, 'accounts/forgotpassword.html')

# Validate Password Reset Token
def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist) as e:
        logger.error(f"Reset password validation error: {e}")
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password.')
        
        # Redirect with uidb64 and token
        return redirect('accounts:resetpassword')
    else:
        messages.error(request, 'This link has expired!')
        return redirect('accounts:login')


# Reset Password
@redirect_if_logged_in
def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password1']
        confirm_password = request.POST['password2']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request  ,'Password reset successfly')
            return redirect('accounts:login')
        else:    
            messages.error(request , 'Password does not match !')
            return redirect('accounts:resetpassword')
    else:    
       return render(request , 'accounts/resetpassword.html')

# User Profile
@login_required
def profile(request, username):
    user = get_object_or_404(Account, username=username)
    is_owner = request.user == user
    return render(request, 'accounts/profile.html', {'user':user, 'is_owner':is_owner})

@login_required
def update_profile(request, username):
    user = get_object_or_404(Account, username=username)  
    profile = user.profile  

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('accounts:profile', username=user.username)  
    else:
        form = ProfileForm(instance=profile)

    context = {
        'form': form,
        'user': user  
    }
    return render(request, 'accounts/update_profile.html', context)