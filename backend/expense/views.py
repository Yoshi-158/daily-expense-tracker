from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *


# SIGNUP
@csrf_exempt
def signup(request):

    if request.method == 'POST':

        data = json.loads(request.body)

        fullname = data.get('FullName')
        email = data.get('Email')
        password = data.get('Password')

        if UserDetail.objects.filter(Email=email).exists():

            return JsonResponse({
                'message': 'Email already exists'
            }, status=400)

        UserDetail.objects.create(
            FullName=fullname,
            Email=email,
            Password=password
        )

        return JsonResponse({
            'message': 'User registered successfully'
        }, status=201)


# LOGIN
@csrf_exempt
def login(request):

    if request.method == 'POST':

        data = json.loads(request.body)

        email = data.get('email')
        password = data.get('password')

        try:

            user = UserDetail.objects.get(
                Email=email,
                Password=password
            )

            return JsonResponse({
                'message': 'Login successful',
                'userId': user.id,
                'userName': user.FullName
            }, status=200)

        except:

            return JsonResponse({
                'message': 'Invalid credentials'
            }, status=400)


# ADD EXPENSE
@csrf_exempt
def add_expense(request):

    if request.method == 'POST':

        data = json.loads(request.body)

        user_id = data.get('UserId')

        expense_date = data.get('ExpenseDate')

        expense_item = data.get('ExpenseItem')

        expense_cost = data.get('ExpenseCost')

        try:

            user = UserDetail.objects.get(id=user_id)

            Expense.objects.create(
                UserId=user,
                ExpenseDate=expense_date,
                ExpenseItem=expense_item,
                ExpenseCost=expense_cost
            )

            return JsonResponse({
                'message': 'Expense added successfully'
            }, status=201)

        except Exception as e:

            return JsonResponse({
                'message': 'Something went wrong',
                'error': str(e)
            }, status=400)


# MANAGE EXPENSE
@csrf_exempt
def manage_expense(request, user_id):

    if request.method == 'GET':

        expenses = Expense.objects.filter(UserId=user_id)

        expense_list = list(expenses.values())

        return JsonResponse(expense_list, safe=False)


# UPDATE EXPENSE
@csrf_exempt
def update_expense(request, expense_id):

    if request.method == 'PUT':

        try:

            expense = Expense.objects.get(id=expense_id)

            data = json.loads(request.body)

            expense.ExpenseDate = data.get('ExpenseDate')

            expense.ExpenseItem = data.get('ExpenseItem')

            expense.ExpenseCost = data.get('ExpenseCost')

            expense.save()

            return JsonResponse({
                'message': 'Expense updated successfully'
            }, status=200)

        except Exception as e:

            return JsonResponse({
                'message': 'Update failed',
                'error': str(e)
            }, status=400)


# DELETE EXPENSE
@csrf_exempt
def delete_expense(request, expense_id):

    if request.method == 'DELETE':

        try:

            expense = Expense.objects.get(id=expense_id)

            expense.delete()

            return JsonResponse({
                'message': 'Expense deleted successfully'
            }, status=200)

        except Exception as e:

            return JsonResponse({
                'message': 'Delete failed',
                'error': str(e)
            }, status=400)

# CHANGE PASSWORD
@csrf_exempt
def change_password(request):

    if request.method == 'PUT':

        try:

            data = json.loads(request.body)

            user_id = data.get('userId')

            old_password = data.get('oldPassword')

            new_password = data.get('newPassword')

            user = UserDetail.objects.get(id=user_id)

            if user.Password != old_password:

                return JsonResponse({

                    'message': 'Old password is incorrect'

                }, status=400)

            user.Password = new_password

            user.save()

            return JsonResponse({

                'message': 'Password updated successfully'

            }, status=200)

        except Exception as e:

            return JsonResponse({

                'message': 'Password update failed',
                'error': str(e)

            }, status=400)