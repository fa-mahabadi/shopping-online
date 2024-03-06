
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View
from .forms import MyRegisterForm, VerifyCodeForm, AddressForm, UserProfile
from .models import MyUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.management.utils import get_random_secret_key
from .tasks import send_otp_email
import redis
import random
import string
from datetime import timedelta
import jwt
from datetime import datetime, timedelta
from rest_framework import generics
from django.views.generic import TemplateView
from rest_framework.permissions import IsAuthenticated
from .models import Address
from .serializers import AddressSerializer
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


def shopping_cart(request):
    return render(request, "shopping_cart.html")

class MyLoginView(LoginView):
    """view for login user and set jwt token in cookie"""

    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.get_user()
        if user is not None:
            secret_key = get_random_secret_key()
            expire_time = datetime.now() + timedelta(days=30)
            payload = {
                "username": user.email,
                "password": user.password,
                "date": int(expire_time.timestamp()),
            }
            token = jwt.encode(payload, secret_key, algorithm="HS256")
            decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
            expire_time = decoded_token["date"]
            if expire_time <= int(datetime.now().timestamp()):
                return HttpResponse("Token has expired. Login not allowed.")
            # Log in  user
            login(self.request, user)

            # Set JWT token in cookie
            response = super().form_valid(form)
            response.set_cookie("jwt_token", token, httponly=True)
            return response
        else:
            return HttpResponse("Invalid username or password")

    def get_success_url(self):
        return reverse_lazy("shopping_cart")

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password")
        return self.render_to_response(self.get_context_data(form=form))


class MyLogoutView(LogoutView):
    """logout user and delete shopping_cart cookie and jwt_token cookie"""

    next_page = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response.delete_cookie("shopping_cart")
        response.delete_cookie("jwt_token")
        return response


class RegisterView(View):
    """register user view"""

    template_name = "registration/register.html"

    def generate_opt_code(self):
        return "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

    def generate_and_store_opt_code(self, email):
        opt_code = self.generate_opt_code()
        redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)
        redis_client.setex(f"opt_code:{email}", timedelta(days=3), opt_code)
        send_otp_email.delay(email, opt_code)

    def post(self, request, *args, **kwargs):

        form = MyRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            myuser = MyUser.objects.filter(email=email).exists()
            if myuser:
                messages.error(request, "this email already use")
            else:
                request.session["register_session"] = {
                    "email": email,
                    "password": password,
                }
                # user = form.save()
                self.generate_and_store_opt_code(email)
                return redirect("verify_code")
        return render(request, "registration/register.html", {"form": form})

    def get(self, request, *args, **kwargs):
        form = MyRegisterForm()
        return render(request, "registration/register.html", {"form": form})

        # expire_opt_code.apply_async(
        #     args=[user_id], countdown=259200
        # )  # 259200 seconds = 3 day

    # @shared_task
    # def expire_opt_code(user_id):
    #     redis_client.delete(f"opt_code:{user_id}")


class Verify_code(View):
    """verify code user"""

    def get(self, request):

        form = VerifyCodeForm()
        return render(request, "registration/verify.html", {"form": form})

    def post(self, request):
        form = VerifyCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            session_email = self.request.session.get("register_session")
            cach_code = redis_client.get(f"opt_code:{session_email}")
            if code == cach_code:
                MyUser.objects.create_user(email=session_email, password=password)
                return redirect("login")
            else:
                messages.error("احراز هویت انجام نشد")
        return render(request, "registration/verify.html", {"form": form})


@login_required
def create_profile(request):
    """create profile user"""
    if request.method == "POST":
        form = UserProfile(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect("shopping_cart")
    else:
        form = UserProfile()
    return render(request, "customer/profile_form.html", {"form": form})


class AddressAPIView(APIView):
    """apiview for get and create address"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        addresses = Address.objects.filter(user=request.user)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressDetailAPIview(APIView):
    """api view for update and delete address"""

    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        address = get_object_or_404(Address, pk=pk)
        serializer = AddressSerializer(address)
        return Response(serializer.data)

    def put(self, request, pk):
        address = get_object_or_404(Address, pk=pk)
        serializer = AddressSerializer(address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        address = get_object_or_404(Address, pk=pk)
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
