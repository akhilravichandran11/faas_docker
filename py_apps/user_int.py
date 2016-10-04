from subprocess import call
import os

print("Hello, How are you? Let us make Cloud Computing great again! ")
return_typ = input("Please enter return type expected ")
func_name = input("Please enter the file name ")
fobj = open(func_name, 'w')

fobj.write("import sys\n")
fobj.write("print( \'Number of arguments:\', len(sys.argv), \'arguments.\')\n")
fobj.write("print(\'Argument List:\', str(sys.argv))\n")

print("Enter the code line by line or enter $ to exit")
prog_src = []
prog_src_ln = input()
while prog_src_ln != "$":
    prog_src.append(prog_src_ln)
    temp = prog_src_ln + "\n"
    fobj.write(temp)
    prog_src_ln = input()

print("Please enter the arguements or press $ to end ")
args = []
val = input()
while val != "$":
    args.append(val)
    val = input()

print(return_typ)
for n in prog_src:
    print(n)

print(args)
fobj.close()

fobj1 = open(func_name)
print(fobj1.read())
fobj1.close()

str1 = ' '.join(args)
#print(str1)
#chk_prog = "Error:"
command_call = 'python ./' + func_name + ' ' + str1
#print(command_call)
chk_prog2 = os.system(command_call + ' | cat > temp_file ')

#print(chk_prog)
if os.stat("temp_file").st_size == 0:
    chk_prog2 = 1
else:
    fobj2 = open('temp_file','r')
    chk_prog = fobj2.read()
    fobj2.close

#print("CheckProgram " + chk_prog)
print(chk_prog2)
if chk_prog2:
    print("Syntax Error")
else:
    print("The Program has compiled successfully")
