
def sum(a):
    sum = a+2
    return sum

eg_list = [5,4]

# Convert to list to make readable
print(list(map(sum,eg_list)))


def sum(a,b):
    sum = a+b
    return sum

eg_list = [5,4,1]
eg_list_b = [-5,-4]

# Convert to list to make readable
print(list(map(sum,eg_list,eg_list_b )))

print("this is the lambda",list(map(lambda a,b:a+b,eg_list,eg_list_b)))