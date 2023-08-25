import string

translator = str.maketrans("","", string.punctuation)

f = ['(1,)', '(3,)']
print(f[0].translate(translator))