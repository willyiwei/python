#!/usr/bin/env python

origin_str = """g fmnc wms bgblr rpylqjyrc gr zw fylb.
rfyrq ufyr amknsrcpq ypc dmp.
bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle.
sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj."""

new_str = '' # Initialize an empty string to contain the temp data

for char in origin_str:
    if char == 'y':
        new_str += 'a'
    elif char == 'z':
        new_str += 'b'
    elif char == '(' or char == ')' or char == ' ' or char == '.' or char == "'":
        new_str += char
    else:
        new_str += chr(ord(char) + 2) # Shift the character by two.
        

print new_str

url_str = 'map'

new_url_str = '' # Initialize an empty string to contain the temp data

for char in url_str:
    if char == 'y':
        new_url_str += 'a'
    elif char == 'z':
        new_url_str += 'b'
    elif char == '(' or char == ')' or char == ' ' or char == '.' or char == "'":
        new_url_str += char
    else:
        new_url_str += chr(ord(char) + 2) # Shift the character by two.
        

print new_url_str


