
import pickle
input_file = open('/home/rxlx/data.dep', 'rb')
decoder = open('/home/rxlx/key.dep', 'rb')

active = True

while active:
    try:
        contents = pickle.load(input_file)
    except EOFError:
        active = False

print(contents)
active = True
while active:
    try:
        message = pickle.load(decoder)
    except EOFError:
        active = False


converted_string = []
for value in contents[:]:
    if value in message:
        #print(value)
        converted_string.append(message[value])
        #print(v, message[v], end='')

#print(message.values())
#print(message.keys())
print(converted_string[:])
str2 = ''.join(str(e) for e in converted_string)
print(str2)
#for char in converted_string[:]:
#    print(char, end='')

print("\n")
#for k, v in message.items():
#    print(k, v)
