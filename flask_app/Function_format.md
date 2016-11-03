- Function Declaration
  Description : Users can create any functions inside the code, But these have to be declared as global functions
  - Example:
    def print1:
      print "test 1"
    def fib_iterative(n):
      i = 0
      j = 1
      k = 0
      while(n>0):
        k = i + j
        i = j
        j = k
        n = n -1
      return k
    global print1,fib_iterative
- Madhat Function Declaration
  Description : Users have to declare the Madhat Function and have their run logic inside it,As this is the only way they can execute thier scripts
  - Example:
    def madhat_func(input_data,output_data):
      print1
      print str(fib_iterative(5))
- Global Data Accessible
  Description : Users can access input_data and manipulate output_data globally inside all functions
  - Input Data
    Description : Users have to give thier required data that they wish to be accessible inside functions in input_data during execute function call
    - Example:
       input_data = {
          "val_1" : 10,
          "val_2" : 5
        }
        def madhat_func(input_data,output_data):
          print1
          print str(fib_iterative(input_data("val_2")))
  - Output Data
    Description : Users can have the output_data to store any data processed and executed in the script
    - Example:
       output_data = {
          "fib_val_1" : 10
        }
        def madhat_func(input_data,output_data):
          print1
          output_data["fib_val_1"] = fib_iterative(input_data("val_1"))
          output_data["fib_val_2"] = fib_iterative(input_data("val_2"))