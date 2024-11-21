from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # 기본 필드: AbstractUser에서 제공
    email = models.EmailField(unique=True)
    # - password (비밀번호)

    # 추가 필드
    is_email_verified = models.BooleanField(default=False)  # 인증 상태 저장
    agree_marketing = models.BooleanField(default=False)  # 개인정보 마케팅 활용 동의
    agree_notifications = models.BooleanField(default=False)  # 알림 메일 및 SMS 수신 동의
    username = models.CharField(max_length=20, unique=True, null=True)
