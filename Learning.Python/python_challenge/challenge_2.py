#!/usr/bin/env python

import string

def main():
	origin_str = '''g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq
	 ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm
	 jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj.'''
	
	url = 'map'

	'''for ch in origin_str:
		if ch.isalpha():
			if ch == 'y':
				print 'a',
			elif ch == 'z':
				print 'b',
			else:
				print unichr(ord(ch) + 2),
		else:
			print ch,'''
	
	t_table = string.maketrans('abcdefghijklmnopqrstuvwxyz', \
			'cdefghijklmnopkrstuvwxyzab')
	t_str = origin_str.translate(t_table)
	new_url = url.translate(t_table)

	print t_str

	print new_url

if __name__ == '__main__':
	main()
