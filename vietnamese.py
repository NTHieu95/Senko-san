# -*- coding: utf8 -*-
import io, sys, urllib3, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

if os.path.exists(os.path.dirname("list.txt")):
    os.remove("list.txt")
# os.makedirs(os.path.dirname("list.txt"))
output = open("list.txt","w+",encoding="utf-8")
output.write("Lê Phương Thảo")
output.close() 