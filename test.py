import threading
from time import *

# numbers = [0,1,2,3,4,5]

# for number in list(numbers):
# 	numbers.remove(number)


# print(numbers)

# print(int(time()))


# # def printit():
# #   threading.Timer(5.0, printit).start()
# #   print("Hello, World!")


# # printit()
count = 0
with open('userlog.txt', "r+") as f:
	lines = f.readlines()

	if lines[-1] == "":
		count = 1
		f.write(str(count)+" AYO PEPE LOL\n")
		print("AYO")
	elif lines[-1] != "":
		split_line = lines[-1].split(';')
		count = int(split_line[0]) + 1
		f.write(str(count)+"\n")
ctimenow = ctime(time())

print(ctimenow)


word_list = ['obytay', 'ikeslay', 'ishay', 'artway']\


for word in word_list:
	word = 'YOLO'

print(word_list)


a = [1, 3, 5]
b = a
a[:] = [x + 2 for x in a]
print(b)
# print (' '.join(word for word in word_list))




# temp ='Thu Apr 15 23:25:02 2021'
# pattern = '%a %b %d %H:%M:%S %Y'

# epoch = int(mktime(strptime(temp, pattern)))

# print(epoch)
