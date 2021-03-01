#CA3 File System

import os


'''

# This is initial experiments on FILE SYSTEM management

'''


# pwd = os.system("pwd")
# print(pwd)

# f = open('practice.txt','w+')
# f.write('test')
# f.close()

# print(os.getcwd())

# print(os.listdir())



# import shutil

# shutil.move('practice.txt','/workspace/General/wk11')

# os.listdir()

# shutil.move('/workspace/General/wk11/practice.txt',os.getcwd())

# os.listdir()



# import send2trash

# print(os.listdir())

# send2trash.send2trash('practice.txt')

# print(os.listdir())



# print(os.getcwd())

# print(os.listdir())

# for folder , sub_folders , files in os.walk("CA2"):

#     print("Currently looking at folder: "+ folder)
#     print('\n')
#     print("THE SUBFOLDERS ARE: ")
#     for sub_fold in sub_folders:
#         print("\t Subfolder: "+sub_fold )

#     print('\n')

#     print("THE FILES ARE: ")
#     for f in files:
#         print("\t File: "+f)
#     print('\n')

# #

for w in os.walk("wk1"):
    print(w)
    print(type(w))

print(os.getcwd())


