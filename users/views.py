from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User #이메일 중복 검사
from .utils import generate_verification_code, send_verification_email  # utils.py에서 함수 가져오기
from django.contrib.auth.hashers import make_password
from users.models import CustomUser
from django.contrib.auth import get_user_model

verification_codes = {}     #이메일과 인증 코드를 임시 저장하는 딕셔너리

#이메일 인증 코드 생성 및 전송
class EmailVerificationView(APIView):
    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        #이메일 중복 체크
        if get_user_model().objects.filter(email=email).exists():    #사용중인 이메일인지 확인
            return Response({"error": "Email is already in use."}, status=status.HTTP_400_BAD_REQUEST)

        #인증 코드 생성 및 저장
        code = generate_verification_code()
        verification_codes[email] = code

        #이메일 전송
        send_verification_email(email, code)
    
        # 인증 완료 후 사용자 생성
        user = CustomUser.objects.create(
            email=email,
            is_email_verified=False,  # 초기에는 이메일 인증 안 된 상태
        )

        return Response({"message": "Verification code sent."}, status=status.HTTP_200_OK)
    
#이메일 인증
class VerifyCodeView(APIView):
    def post(self, request):
        email = request.data.get("email").lower()
        code = request.data.get("code")

        if not email or not code:
            return Response({"error": "Email and code are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        #이메일로 저장된 인증 코드 가져오기
        stored_code = verification_codes.get(email)
        if stored_code is None:
            return Response({"error": "No code found for this email."}, status=status.HTTP_400_BAD_REQUEST)
        
        #저장된 코드와 입력받은 코드 비교(형변환)
        if str(stored_code) == str(code):
            #이메일 인증상태 업데이트
            user = CustomUser.objects.filter(email=email).first()
            if user:
                user.is_email_verified = True
                user.save()
                del verification_codes[email]
                return Response({"message": "Email verified."}, status=status.HTTP_200_OK)
        
        #인증코드 불일치
        return Response({"error": "Invalid code."}, status=status.HTTP_400_BAD_REQUEST)

# #회원가입
class RegisterView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        confirm_password = request.data.get("confirm_password")
        username = request.data.get("username")
        agree_marketing = request.data.get("agree_marketing")
        agree_notifications = request.data.get("agree_notifications")

        #필수 필드 검증
        if not email or not password or not confirm_password  or not username:
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        #비밀번호 확인
        if password != confirm_password:
            return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)
        
        #이메일 인증 확인
        user = CustomUser.objects.filter(email=email).first()
        if not user:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        if not user.is_email_verified:
            return Response({"error": "Email not verified."}, status=status.HTTP_400_BAD_REQUEST)
        
        #이메일 인증된 경우, 사용자 정보 업데이트
        user.username = username
        user.password = make_password(password)  # user.set_password(password)  #비밀번호 암호화
        user.agree_marketing = agree_marketing
        user.agree_notifications = agree_notifications
        user.save()

        return Response({"message": "Registration successful."}, status=status.HTTP_201_CREATED)
