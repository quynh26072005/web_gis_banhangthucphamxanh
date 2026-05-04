"""
Utilities để gửi email
"""
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_verification_email(email, otp_code, username):
    """
    Gửi email xác thực đăng ký
    """
    subject = 'Xác thực đăng ký tài khoản - Clean Food GIS'
    
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                       color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
            .otp-code {{ font-size: 32px; font-weight: bold; color: #667eea; 
                         text-align: center; padding: 20px; background: white; 
                         border-radius: 10px; margin: 20px 0; letter-spacing: 5px; }}
            .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
            .warning {{ background: #fff3cd; border-left: 4px solid #ffc107; 
                        padding: 15px; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌿 Clean Food GIS</h1>
                <p>Xác thực đăng ký tài khoản</p>
            </div>
            <div class="content">
                <p>Xin chào <strong>{username}</strong>,</p>
                <p>Cảm ơn bạn đã đăng ký tài khoản tại Clean Food GIS!</p>
                <p>Mã OTP của bạn là:</p>
                <div class="otp-code">{otp_code}</div>
                <div class="warning">
                    <strong>⚠️ Lưu ý:</strong>
                    <ul>
                        <li>Mã OTP có hiệu lực trong <strong>10 phút</strong></li>
                        <li>Không chia sẻ mã này với bất kỳ ai</li>
                        <li>Nếu bạn không yêu cầu đăng ký, vui lòng bỏ qua email này</li>
                    </ul>
                </div>
                <p>Trân trọng,<br><strong>Đội ngũ Clean Food GIS</strong></p>
            </div>
            <div class="footer">
                <p>© 2026 Clean Food GIS. All rights reserved.</p>
                <p>Email này được gửi tự động, vui lòng không trả lời.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    plain_message = f"""
    Xin chào {username},
    
    Cảm ơn bạn đã đăng ký tài khoản tại Clean Food GIS!
    
    Mã OTP của bạn là: {otp_code}
    
    Lưu ý:
    - Mã OTP có hiệu lực trong 10 phút
    - Không chia sẻ mã này với bất kỳ ai
    - Nếu bạn không yêu cầu đăng ký, vui lòng bỏ qua email này
    
    Trân trọng,
    Đội ngũ Clean Food GIS
    """
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_password_reset_email(email, otp_code, username):
    """
    Gửi email reset password
    """
    subject = 'Đặt lại mật khẩu - Clean Food GIS'
    
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                       color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
            .otp-code {{ font-size: 32px; font-weight: bold; color: #f5576c; 
                         text-align: center; padding: 20px; background: white; 
                         border-radius: 10px; margin: 20px 0; letter-spacing: 5px; }}
            .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
            .warning {{ background: #fff3cd; border-left: 4px solid #ffc107; 
                        padding: 15px; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔐 Clean Food GIS</h1>
                <p>Đặt lại mật khẩu</p>
            </div>
            <div class="content">
                <p>Xin chào <strong>{username}</strong>,</p>
                <p>Chúng tôi nhận được yêu cầu đặt lại mật khẩu cho tài khoản của bạn.</p>
                <p>Mã OTP của bạn là:</p>
                <div class="otp-code">{otp_code}</div>
                <div class="warning">
                    <strong>⚠️ Lưu ý:</strong>
                    <ul>
                        <li>Mã OTP có hiệu lực trong <strong>10 phút</strong></li>
                        <li>Không chia sẻ mã này với bất kỳ ai</li>
                        <li>Nếu bạn không yêu cầu đặt lại mật khẩu, vui lòng bỏ qua email này</li>
                        <li>Để bảo mật tài khoản, hãy đổi mật khẩu ngay</li>
                    </ul>
                </div>
                <p>Trân trọng,<br><strong>Đội ngũ Clean Food GIS</strong></p>
            </div>
            <div class="footer">
                <p>© 2026 Clean Food GIS. All rights reserved.</p>
                <p>Email này được gửi tự động, vui lòng không trả lời.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    plain_message = f"""
    Xin chào {username},
    
    Chúng tôi nhận được yêu cầu đặt lại mật khẩu cho tài khoản của bạn.
    
    Mã OTP của bạn là: {otp_code}
    
    Lưu ý:
    - Mã OTP có hiệu lực trong 10 phút
    - Không chia sẻ mã này với bất kỳ ai
    - Nếu bạn không yêu cầu đặt lại mật khẩu, vui lòng bỏ qua email này
    
    Trân trọng,
    Đội ngũ Clean Food GIS
    """
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
