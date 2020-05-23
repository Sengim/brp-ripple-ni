import random

def generate_string():
    i = 0
    flag = True
    return_string = "PL," + str(random.randint(0, 1)) + " "
    k = 1
    while flag and i < 4:

        #if random.randint(i, 4) == 4:
         #   return_string = return_string + "P,1 \r\n"
          #  return return_string
        #return_string = return_string + "P,0 "
        for j in range(1, 5):
            if random.randint(0, 4) > i:
                l = k + 1
                k = k + 1
            else:
                l = k # random.randint(max(k-1, 1), k)
            return_string += "P," + str(l) + "," + str(j) + " "
        i = i + 1
        if random.randint(1, 8) == 8:
            return_string = return_string + "PL," + str(1) + " "
            return_string = return_string + "\r\n"
            return return_string

    return_string = return_string + "\r\n"
    return return_string

def classify_string(inputstring):
    array = [-1, -1, -1, -1]
    split_string = inputstring.split(" ")
    for l in split_string:
        nm = l.split(",")
        if nm[0] == "PL" and int(nm[1]) > 0:
            return False
        elif nm[0] == "P":
            #if int(nm[1]) == 1:
             #   return True
            sender = int(nm[2]) - 1
            data = int(nm[1])
            array[sender] = data
        if check_equaltity_arr(array):
            return True
    return False


def check_equaltity_arr(array):
    k = array[0]
    for i in array:
        if i == -1 or i != k:
            return False
    return True


file_obj = open("data.txt", "w+")

k = 0
l = 20
total = 66
resultstring = str(l) + " 66 \r\n"
for i in range(l):
    inputstring = generate_string()
    count = len(inputstring.split(" ")) - 1
    if classify_string(inputstring):
        temp = "1 " + str(count) + " " + inputstring
        k = k + 1
    else:
        temp = "0 " + str(count) + " " + inputstring
    print(temp)
    resultstring = resultstring + temp
file_obj.write(resultstring)





