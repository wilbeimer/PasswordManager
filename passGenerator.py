from random import *

keys = """`~1!2@3#4$5%6^7&8*9(0)-_=+qQwWeErRtTyYuUiIoOpP[{]}\|aAsSdDfFgGhHjJkKlL;:'"zZcCvVbBnNmM,<.>/?"""

password = ''

for i in range(16):
    i = keys[randrange(0,len(keys)-1)]
    password += i

print(password)