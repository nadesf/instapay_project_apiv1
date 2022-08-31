import string 
import threading
import random 
import time

def function_one():
    time.sleep(3)
    print("Bonjour")

def hello():

    th1 = threading.Thread(target=function_one)
    th1.start()

    return "End Of My Program !"

def hackerman(b):
    b = 2

a = 3

hackerman(a)
print(a)