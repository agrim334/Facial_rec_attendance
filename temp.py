import re

name = 'asdads.jpg'
pat = re.compile('[A-Za-z]+\.')
name = pat.match(name)[0]
name = name[:-2] 
print(name)