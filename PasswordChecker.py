import requests
import hashlib
import sys

def request_api_check(query_char):
		url='https://api.pwnedpasswords.com/range/'+query_char
		response=requests.get(url)
		if response.status_code!=200:
			raise RuntimeError(f'error in prossesing request {response.status_code}, try API later!!!')
		return response

def get_password_leaks_count(hashes,hash_to_check):    #hash_to_check is the tail end
	hashes=(line.split(':') for line in hashes.text.splitlines())
	for h,count in hashes:
		if h==hash_to_check:
			return count
	return None

def pwned_api_check(password):
	sha1password=hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
	first5_char,tail=sha1password[:5],sha1password[5:]
	res=request_api_check(first5_char)
	#print(res)
	return get_password_leaks_count(res,tail)

def main(args):
	for password in args:
		count=pwned_api_check(password)
		if count:
			print(f'{password} was found {count} times, time to change your password!!')
		else:
			print(f'{password} was not found, you are good to GO!!!')
	return "donee!!!"

main(sys.argv[1:])
