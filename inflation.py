import sys
import re

from datetime import datetime
from requests import get

#https://data.bls.gov/cgi-bin/cpicalc.pl?cost1=123&year1=201101&year2=202409
base_uri = "https://data.bls.gov/cgi-bin/cpicalc.pl?cost1={}&year1={}{}&year2={}{}"

rgx_amount = re.compile(r'(\$)?(,)?\d+([.]\d\d)?')
rgx_result = re.compile(r'id=\"answer\".+\$(.+)<\/span.+$', re.M | re.I)

def validate_month(month):
	return month > 0 and month <= 12

def validate_year(year):
	c_year = datetime.now().year
	return year > 1912 and year <= c_year

def validate_input(first_year, second_year, cost):
	y1,m1 = first_year
	y2,m2 = second_year

	y1 = validate_year(y1)
	y2 = validate_year(y2)

	m1 = validate_month(m1)
	m2 = validate_month(m2)

	return y1 and y2 and m1 and m2

def form_uri(first_year, second_year, cost):
	global base_uri

	y1,m1 = first_year
	y2,m2 = second_year

	if m1 < 10:
		m1 = '0' + str(m1)

	if m2 < 10:
		m2 = '0' + str(m2)

	return base_uri.format(cost, y1, m1, y2, m2)

def submit_post(uri):
	#print(f"uri {uri}")
	r = get(uri)
	if r.status_code != 200:
		return None
	return r.content.decode('utf-8')

def parse_response(response):
	global rgx

	match = re.search(rgx_result, response)
	if not match:
		print('Could not find result.')
		return
	print(match.group(1))

def parse_amount(amount):
	if not re.match(rgx_amount, amount):
		return -1.0
	return float(amount.replace('$','').replace(',',''))

def main():
	print("Enter in first month (01-12):")
	month1 = int(input(''))
	if not validate_month(month1):
		print("Could not validate input")
		return

	print("Enter in first year (1913-2024):")
	year1 = int(input(''))
	if not validate_year(year1):
		print("Could not validate input")
		return

	print("Enter in second month (01-12):")
	month2 = int(input(''))
	if not validate_month(month2):
		print("Could not validate input")
		return

	print("Enter in second year (1913-2024):")
	year2 = int(input(''))
	if not validate_year(year2):
		print("Could not validate input")
		return

	print("Enter in dollar amount:")
	amount = str(input(''))
	amount = parse_amount(amount)

	if amount == -1.0:
		print("Could not validate dollar amount")
		return

	if not validate_input([year1,month1], [year2,month2], amount):
		print("Could not validate input")
		return

	uri = form_uri([year1,month1], [year2,month2], amount)
	resp = submit_post(uri)
	parse_response(resp)

if __name__ == "__main__":
	main()
