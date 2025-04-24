import pandas as pd
import os
from django.conf import settings

# Use absolute path for CSV file
csv_path = os.path.join(settings.BASE_DIR, 'tseamcet.csv')

# Load CSV file once when module is imported
try:
	df = pd.read_csv(csv_path)
except Exception as e:
	print(f"Error loading CSV file: {e}")
	df = pd.DataFrame()  # Empty DataFrame as fallback

def predict(rank,gender,caste,branch):
	if branch=='None':
		val=df[df['rank']>=rank]
		val_x=val[val['gender']==gender]
		val_y=val_x[val_x['caste']==caste]
		
		temp=val_y
	else:
		val=df[df['rank']>=rank]
		val_x=val[val['gender']==gender]
		val_y=val_x[val_x['caste']==caste]
		val_z=val_y[val_y['branch']==branch]
		
		temp=val_z
	y=temp.sort_values(by='rank', ascending = True)
	z=y.drop_duplicates(subset = ["college","branch"],keep='last')
	return z

def list_of_colleges():
	res=df.college.unique().tolist()
	return res

def branch_list(college):
	college = df[df['college']==college]
	branches = college.branch.unique().tolist()
	return branches

def fees(college):
	college = df[df['college']==college]
	return college.fee.unique().tolist()[0]

