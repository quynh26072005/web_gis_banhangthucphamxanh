"""
Views cho xác thực email và reset password
"""
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.conf import settings

from food_store.models import EmailVerification, PasswordReset, Customer
from food_store.email_utils import send_verification_email, send_password_reset_email


def register_step1(request):
    """
    Bước 1: Nhập thông tin đăng ký và gửi OTP
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        phone = request.POST.get('phone', '')
        
        # Validation
        if not all([username, email, password, password_confirm]):
            messages.error(request, 'Vui lòng điền đầy đủ thông tin!')
            return render(request, 'auth/register_step1.html')
        
        if password != password_confirm:
            messages.error(request, 'Mật khẩu xác nhận không khớp!')
            return render(request, 'auth/register_step1.html')
        
        if len(password) < 6:
            messages.error(request, 'Mật khẩu phải có ít nhất 6 ký tự!')
            return render(request, 'auth/register_step1.html')
        
        # Kiểm tra username đã tồn tại
        if User.objects.filter(username=username).exists():
            messages.error(request, f'Username "{username}" đã tồn tại!')
            return render(request, 'auth/register_step1.html')
        
        # Kiểm tra email đã tồn tại
        if User.objects.filter(email=email).exists():
            messages.error(request, f'Email "{email}" đã được đăng ký!')
            return render(request, 'auth/register_step1.html')
        
        # Tạo mã xác thực
        verification = EmailVerification.create_verification(
            email=email,
            username=username,
            password=make_password(password),  # Hash password
            first_name=first_name,
            last_name=last_name,
            phone=phone
        )
        
        # Gửi email
        if send_verification_email(email, verification.otp_code, username):
            messages.success(request, f'Mã OTP đã được gửi đến {email}. Vui lòng kiểm tra email!')
            return redirect('food_store:register_step2', verification_id=verification.id)
        else:
            messages.error(request, 'Không thể gửi email. Vui lòng thử lại!')
            verification.delete()
    
    return render(request, 'auth/register_step1.html')


def register_step2(request, verification_id):
    """
    Bước 2: Nhập mã OTP để xác thực
    """
    try:
        verification = EmailVerification.objects.get(id=verification_id, is_verified=False)
    except EmailVerification.DoesNotExist:
        messages.error(request, 'Mã xác thực không hợp lệ!')
        return redirect('food_store:register_step1')
    
    # Kiểm tra hết hạn
    if verification.is_expired():
        messages.error(request, 'Mã OTP đã hết hạn! Vui lòng đăng ký lại.')
        verification.delete()
        return redirect('food_store:register_step1')
    
    if request.method == 'POST':
        otp_code = request.POST.get('otp_code')
        
        if not otp_code:
            messages.error(request, 'Vui lòng nhập mã OTP!')
            return render(request, 'auth/register_step2.html', {'verification': verification})
        
        # Kiểm tra số lần thử
        if not verification.can_retry():
            messages.error(request, 'Bạn đã nhập sai quá nhiều lần! Vui lòng đăng ký lại.')
            verification.delete()
            return redirect('food_store:register_step1')
        
        # Kiểm tra mã OTP
        if otp_code == verification.otp_code:
            # Tạo user
            user = User.objects.create(
                username=verification.username,
                email=verification.email,
                password=verification.password,  # Đã hash rồi
                first_name=verification.first_name,
                last_name=verification.last_name
            )
            
            # Tạo Customer profile
            Customer.objects.create(
                user=user,
                phone=verification.phone
            )
            
            # Đánh dấu đã xác thực
            verification.is_verified = True
            verification.save()
            
            # Tự động đăng nhập
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            messages.success(request, f'Đăng ký thành công! Chào mừng {user.username}!')
            return redirect('food_store:home')
        else:
            # Sai mã OTP
            verification.attempts += 1
            verification.save()
            
            remaining = 5 - verification.attempts
            messages.error(request, f'Mã OTP không đúng! Còn {remaining} lần thử.')
    
    context = {
        'verification': verification,
        'remaining_time': (verification.expires_at - verification.created_at).seconds // 60
    }
    return render(request, 'auth/register_step2.html', context)


def resend_otp(request, verification_id):
    """
    Gửi lại mã OTP
    """
    try:
        verification = EmailVerification.objects.get(id=verification_id, is_verified=False)
    except EmailVerification.DoesNotExist:
        messages.error(request, 'Mã xác thực không hợp lệ!')
        return redirect('food_store:register_step1')
    
    # Tạo mã mới
    new_verification = EmailVerification.create_verification(
        email=verification.email,
        username=verification.username,
        password=verification.password,
        first_name=verification.first_name,
        last_name=verification.last_name,
        phone=verification.phone
    )
    
    # Gửi email
    if send_verification_email(new_verification.email, new_verification.otp_code, new_verification.username):
        messages.success(request, 'Mã OTP mới đã được gửi đến email của bạn!')
        return redirect('food_store:register_step2', verification_id=new_verification.id)
    else:
        messages.error(request, 'Không thể gửi email. Vui lòng thử lại!')
        return redirect('food_store:register_step2', verification_id=verification_id)


def forgot_password_step1(request):
    """
    Bước 1: Nhập email để nhận mã OTP reset password
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        
        if not email:
            messages.error(request, 'Vui lòng nhập email!')
            return render(request, 'auth/forgot_password_step1.html')
        
        # Kiểm tra email có tồn tại không
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Email này chưa được đăng ký!')
            return render(request, 'auth/forgot_password_step1.html')
        
        # Tạo mã reset
        reset = PasswordReset.create_reset(user)
        
        # Gửi email
        if send_password_reset_email(email, reset.otp_code, user.username):
            messages.success(request, f'Mã OTP đã được gửi đến {email}. Vui lòng kiểm tra email!')
            return redirect('food_store:forgot_password_step2', reset_id=reset.id)
        else:
            messages.error(request, 'Không thể gửi email. Vui lòng thử lại!')
            reset.delete()
    
    return render(request, 'auth/forgot_password_step1.html')


def forgot_password_step2(request, reset_id):
    """
    Bước 2: Nhập mã OTP và mật khẩu mới
    """
    try:
        reset = PasswordReset.objects.get(id=reset_id, is_used=False)
    except PasswordReset.DoesNotExist:
        messages.error(request, 'Mã reset không hợp lệ!')
        return redirect('food_store:forgot_password_step1')
    
    # Kiểm tra hết hạn
    if reset.is_expired():
        messages.error(request, 'Mã OTP đã hết hạn! Vui lòng thử lại.')
        reset.delete()
        return redirect('food_store:forgot_password_step1')
    
    if request.method == 'POST':
        otp_code = request.POST.get('otp_code')
        new_password = request.POST.get('new_password')
        password_confirm = request.POST.get('password_confirm')
        
        if not all([otp_code, new_password, password_confirm]):
            messages.error(request, 'Vui lòng điền đầy đủ thông tin!')
            return render(request, 'auth/forgot_password_step2.html', {'reset': reset})
        
        if new_password != password_confirm:
            messages.error(request, 'Mật khẩu xác nhận không khớp!')
            return render(request, 'auth/forgot_password_step2.html', {'reset': reset})
        
        if len(new_password) < 6:
            messages.error(request, 'Mật khẩu phải có ít nhất 6 ký tự!')
            return render(request, 'auth/forgot_password_step2.html', {'reset': reset})
        
        # Kiểm tra số lần thử
        if not reset.can_retry():
            messages.error(request, 'Bạn đã nhập sai quá nhiều lần! Vui lòng thử lại.')
            reset.delete()
            return redirect('food_store:forgot_password_step1')
        
        # Kiểm tra mã OTP
        if otp_code == reset.otp_code:
            # Đổi mật khẩu
            user = reset.user
            user.set_password(new_password)
            user.save()
            
            # Đánh dấu đã sử dụng
            reset.is_used = True
            reset.save()
            
            messages.success(request, 'Đổi mật khẩu thành công! Vui lòng đăng nhập.')
            return redirect('food_store:custom_login')
        else:
            # Sai mã OTP
            reset.attempts += 1
            reset.save()
            
            remaining = 5 - reset.attempts
            messages.error(request, f'Mã OTP không đúng! Còn {remaining} lần thử.')
    
    context = {
        'reset': reset,
        'remaining_time': (reset.expires_at - reset.created_at).seconds // 60
    }
    return render(request, 'auth/forgot_password_step2.html', context)


def resend_reset_otp(request, reset_id):
    """
    Gửi lại mã OTP reset password
    """
    try:
        reset = PasswordReset.objects.get(id=reset_id, is_used=False)
    except PasswordReset.DoesNotExist:
        messages.error(request, 'Mã reset không hợp lệ!')
        return redirect('food_store:forgot_password_step1')
    
    # Tạo mã mới
    new_reset = PasswordReset.create_reset(reset.user)
    
    # Gửi email
    if send_password_reset_email(new_reset.email, new_reset.otp_code, new_reset.user.username):
        messages.success(request, 'Mã OTP mới đã được gửi đến email của bạn!')
        return redirect('food_store:forgot_password_step2', reset_id=new_reset.id)
    else:
        messages.error(request, 'Không thể gửi email. Vui lòng thử lại!')
        return redirect('food_store:forgot_password_step2', reset_id=reset_id)
