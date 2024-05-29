dict_test = {'a':2,'b':4}

dict_test_2 = dict_test

dict_test['a'] = 4
print(dict_test_2)


dict_list = [2,4]

dict_list_2 = dict_list
print(dict_list)
dict_list[0] = 8
print(dict_list_2)
print(dict_list)

a = 2

b = a

a =4

print(a,b)