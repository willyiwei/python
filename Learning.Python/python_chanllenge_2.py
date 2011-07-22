original_str = """g fmnc wms bgblr rpylqjyrc gr zw fylb.
rfyrq ufyr amknsrcpq ypc dmp.
bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle.
sqgle qrpgle.kyicrpylq() gq pcamkkclbcb.
lmu ynnjw ml rfc spj."""

char_list = []

for char in original_str:
    if char == 'k':
        char_list.append('m')
    elif char == 'o':
        char_list.append('q')
    elif char == 'e':
        char_list.append('g')
    else:
        char_list.append(char)

print str(char_list)
