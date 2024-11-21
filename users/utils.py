import random
from django.core.mail import send_mail

def generate_verification_code():
    """6자리 인증 코드 생성"""
    return f"{random.randint(100000, 999999)}"  # 6자리 숫자 코드

def send_verification_email(email, code):
    """이메일로 인증 코드 전송"""
    send_mail(
        subject="Email Verification Code",
        message=f"Your verification code is: {code}",
        from_email="rmfosem0202@gmail.com",
        recipient_list=[email],
    )
