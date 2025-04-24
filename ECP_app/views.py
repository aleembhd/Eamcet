from django.shortcuts import render, redirect
from .demo import *
import numpy
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

# Authentication check decorator
def auth_required(view_func):
	def wrapper(request, *args, **kwargs):
		# Check if user is authenticated (has valid session)
		if not request.session.get('is_authenticated', False):
			return redirect('login')
		return view_func(request, *args, **kwargs)
	return wrapper

def login_view(request):
	return render(request, 'login.html')

def signup_view(request):
	return render(request, 'signup.html')

@csrf_exempt
def auth_callback(request):
	if request.method == 'POST':
		try:
			data = json.loads(request.body)
			email = data.get('email')
			action = data.get('action', 'login')
			
			if not email:
				return JsonResponse({'success': False, 'error': 'Email is required'})
				
			# For simplicity in this demo:
			# 1. We're not validating passwords against a database
			# 2. We're storing minimal user info in the session
			
			# Store authentication in session
			request.session['is_authenticated'] = True
			request.session['user_email'] = email
			
			if action == 'signup':
				request.session['user_name'] = data.get('name', '')
				
			return JsonResponse({'success': True})
		except Exception as e:
			return JsonResponse({'success': False, 'error': str(e)})
	return JsonResponse({'success': False, 'error': 'Invalid request method'})

def logout_view(request):
	# Clear session
	request.session.flush()
	return redirect('login')

@auth_required
@csrf_exempt
def homepage(request):
	if request.method == 'POST':
		rank=int(request.POST.get('rank'))
		gender=str(request.POST.get('gender')) 
		caste=str(request.POST.get('caste'))
		branch=str(request.POST.get('branch'))

		# print(rank,gender,caste,branch)
		val=predict(rank,gender,caste,branch)
		
		vals=val.to_numpy().tolist()
		# print(vals)
		context ={'values':vals}
		return render(request,'results.html',context=context)

	return render(request,'homepagee.html')

@auth_required
def college_list(request):
	res=list_of_colleges()
	context={'colleges':res}
	return render(request,'colleges_list.html',context)

@auth_required
def college_branch(request,pk):
	branch=branch_list(pk)
	context={'branches':branch,'Name':pk}
	return render(request,'college.html',context)

@auth_required
def college_branch_student(request,pk1,pk2):
	li=college_branch_data(pk1,pk2)
	li=li.to_numpy().tolist()
	total=len(li)
	context={'data':li,'Name':pk1,'Branch':pk2,'total':total}
	return render(request,'college_branch_student.html',context)

@auth_required
def college_branch_student_view(request):
	try:
		# Use the absolute path to your CSV file
		df = pd.read_csv('tseamcet.csv')
		
		# Sample data processing (modify according to your CSV structure)
		data = []
		for index, row in df.iterrows():
			# Assuming your CSV has columns like rank, gender, category
			data.append([
				row['rank'],
				row['gender'],
				row['category']
			])
		
		context = {
			'Name': 'Test College',
			'Branch': 'Computer Science',
			'data': data,
			'total': len(data)
		}
		return render(request, 'college_branch_student.html', context)
	except Exception as e:
		print(f"Error: {e}")
		return render(request, 'college_branch_student.html', {'error': str(e)})

@auth_required
def college_guide(request):
	return render(request, 'college_guide.html')

@csrf_exempt
def chat(request):
	if request.method == 'POST':
		import json
		data = json.loads(request.body)
		user_message = data.get('message', '').lower()
		
		# Simple college guidance logic
		response = generate_college_response(user_message)
		
		return JsonResponse({'response': response})
	
	return JsonResponse({'error': 'Invalid request method'}, status=400)

def generate_college_response(user_message):
	# Keywords for different college aspects
	admission_keywords = ['admission', 'apply', 'entrance', 'exam', 'eamcet', 'rank', 'cutoff']
	branch_keywords = ['branch', 'department', 'course', 'stream', 'engineering', 'cse', 'ece', 'mechanical']
	fees_keywords = ['fees', 'cost', 'expense', 'payment', 'scholarship', 'financial']
	placement_keywords = ['placement', 'job', 'salary', 'package', 'career', 'company']
	college_keywords = ['college', 'university', 'institute', 'campus', 'hostel', 'facility']
	
	# Check for keywords in the user message
	if any(keyword in user_message for keyword in admission_keywords):
		return "For college admissions, you'll need to consider your EAMCET rank, category, and preferred branch. Would you like to know the cutoff ranks for specific colleges?"
	
	elif any(keyword in user_message for keyword in branch_keywords):
		return "Different engineering branches have different cutoff ranks and career prospects. Which branch are you interested in? I can help you understand the opportunities and requirements."
	
	elif any(keyword in user_message for keyword in fees_keywords):
		return "College fees vary based on the type of college (government/private) and available scholarships. Would you like to know about specific college fees or scholarship opportunities?"
	
	elif any(keyword in user_message for keyword in placement_keywords):
		return "Placement opportunities vary by college and branch. I can help you understand the placement statistics and average packages for different colleges. Which aspect would you like to know more about?"
	
	elif any(keyword in user_message for keyword in college_keywords):
		return "I can help you compare different colleges based on factors like location, facilities, placements, and fees. What aspects of colleges are most important to you?"
	
	elif 'rank' in user_message or 'score' in user_message or 'marks' in user_message:
		return "Your rank is crucial for college admission. Based on your rank and category, I can help you find colleges where you have a good chance of admission. What's your rank and category?"
	
	elif 'compare' in user_message or 'difference' in user_message or 'better' in user_message:
		return "I can help you compare colleges based on various factors like placements, infrastructure, fees, and location. Which colleges would you like to compare?"
	
	elif 'help' in user_message or 'guide' in user_message or 'suggest' in user_message:
		return "I can help you with college selection based on your rank, preferred branch, and other preferences. What would you like to know about?"
	
	else:
		return "I'm here to help you with college-related queries. I can provide information about admissions, branches, fees, placements, and more. What specific information are you looking for?"
