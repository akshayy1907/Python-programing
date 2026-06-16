# Sample dictionary
a = {'apple': 3, 'banana': 4, 'strawbeery': 7, 'grape': 1}
# Sorting using sorted() method
b = {key: value for key, value in sorted(a.items(), key=lambda item: item[1])}
print(b)