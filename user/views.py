from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model 
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomAuthenticationForm, SignUpForm, UserProfileUpdateForm
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET

User = get_user_model()

@require_GET
def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow:/",
        "Disallow:/admin/",
        f"Sitemap: https://{request.get_host()}/sitemap.xml"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

# 회원가입
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # 사용자 생성
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('closet:dashboard')
    else:
        form = SignUpForm()
    return render(request, 'user/signup.html', {'form': form})

# 로그아웃
def logout_view(request):
    logout(request)
    return redirect('closet:dashboard')

# 로그인
def login_view(request):
    # 이미 로그인된 사용자는 대시보드로 리다이렉트
    if request.user.is_authenticated:
        return redirect('closet:dashboard')
        
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                # next 파라미터가 있으면 해당 URL로, 없으면 대시보드로
                next_url = request.GET.get('next', 'closet:dashboard')
                return redirect(next_url)
            else:
                return render(request, 'user/login.html', {'form': form, 'invalid_creds': True})
    else:
        form = CustomAuthenticationForm()
    return render(request, 'user/login.html', {'form': form})

# 대시보드
@login_required
def dashboard_view(request):
    username = request.user.nickname  # CustomUser 모델의 nickname 필드 사용
    return render(request, "closet/home/dashboard.html", {"user": request.user})

# 사용자 프로필 보기
@login_required
def user_profile_view(request):
    if request.method == "POST":
        try:
            # POST 데이터와 FILES 데이터를 모두 처리
            form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                user = form.save(commit=False)
                
                # 프로필 이미지 처리
                if 'profile_image' in request.FILES:
                    user.profile_image = request.FILES['profile_image']
                elif not user.profile_image:  # 이미지가 없는 경우
                    user.profile_image = None
                
                user.save()
                return JsonResponse({"success": True})
            return JsonResponse({"success": False, "errors": form.errors})
        except Exception as e:
            print(f"Error: {str(e)}")  # 디버깅용
            return JsonResponse({"success": False, "errors": str(e)})
    
    return render(request, "user/user_profile.html", {"user": request.user})

# 사용자 프로필 수정
@login_required
def edit_profile_view(request):
    """프로필 수정 뷰"""
    if request.method == "POST":
        try:
            form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                user = form.save(commit=False)
                if 'profile_image' in request.FILES:
                    user.profile_image = request.FILES['profile_image']
                elif not user.profile_image:
                    user.profile_image = None
                user.save()
                return JsonResponse({"success": True})
            return JsonResponse({"success": False, "errors": form.errors})
        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({"success": False, "errors": str(e)})
    
    return render(request, "user/edit_profile.html", {"user": request.user})

@login_required
def view_profile_view(request):
    """프로필 조회 뷰"""
    return render(request, "user/view_profile.html", {"user": request.user})

def index_view(request):
    """
    최초 진입점. 로그인 상태에 따라 대시보드 또는 로그인 페이지를 보여줌
    """
    if request.user.is_authenticated:
        return render(request, "closet/home/dashboard.html", {"user": request.user})
    
    # 로그인되지 않은 경우 로그인 폼 준비
    form = CustomAuthenticationForm()
    return render(request, 'user/login.html', {'form': form})