#!/usr/bin/env python
# Filename: guess_number.py

def main():
	number = 55
	
	while(True):
		input_num = int(raw_input('Enter a number: '))
	
		if input_num == number:
			print 'Congratulations, you hit the answer!'
			break
		elif input_num < number:
			print 'Too low, please input another number to try'
		else:
			print 'Too high, please input another number to try'
	
	print 'Done'

if __name__ == '__main__':
	main()
