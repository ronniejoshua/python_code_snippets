# Generator Function - Returns a Generator Object
def even_integers_generator(n):
    for i in range(n):
        if i % 2 == 0:
            yield i


# Generator Expression
even_integers = (n for n in range(10) if n % 2 == 0)


# list of mixed format numbers
numbers = [7, 22, 4.5, 99.7, "3", "5"]

# convert numbers to integers using expression
integers = (int(n) for n in numbers)


names_list = ["Charlie", "Cassandra"]

# Converts names to uppercase - List Comprehension
uppercase_names = [name.upper() for name in names_list]

# Converts names to uppercase - Generator Expression
uppercase_names = (name.upper() for name in names_list)

# Nested Generators - Generator Expression
reverse_uppercase = (name[::-1] for name in (name.upper() for name in names_list))

# Generators - Pipelines - Generator Expression
uppercase = (name.upper() for name in names_list)
reverse_uppercase = (name[::-1] for name in uppercase)


# Fibonacci Sequence Generator
def fibonacci_gen():
    trailing, lead = 0, 1
    while True:
        yield lead
        trailing, lead = lead, trailing + lead


fib = fibonacci_gen()
next(fib)

for _ in range(10):
    next(fib)

# GENERATOR PIPELINES
# -------------------

# using generators to find the longest name
full_names = (name.strip() for name in open("names.txt"))
lengths = ((name, len(name)) for name in full_names)
longest = max(lengths, key=lambda x: x[1])

# iternation - 2
# adding separate_names generator as another stage in pipeline
def separate_names(names):
    for full_name in names:
        for name in full_name.split(" "):
            yield name


full_names = (name.strip() for name in open("names.txt"))
names = separate_names(full_names)
lengths = ((name, len(name)) for name in names)
longest = max(lengths, key=lambda x: x[1])

# iteration 3 - functional form
def get_longest(namelist):
    full_names = (name.strip() for name in open(namelist))
    names = separate_names(full_names)
    lengths = ((name, len(name)) for name in names)
    return max(lengths, key=lambda x: x[1])




# Basic contextmanager Framework
from contextlib import contextmanager

@contextmanager
def simple_context_manager(obj):
    try:
        # Setup Code

        # yield Causes the context manager to pause and yeild the control
        # back to the caller to do a particular action/actions
        yield
    finally:
        # Wrap up Code

class SomeObj(object):
    def __init__(self, arg):
        self.obj_attribute = arg

from contextlib import contextmanager

@contextmanager
def simple_context_manager(obj):
    try:
        # Setup Code
        obj.obj_attribute += 1
        # yield Causes the context manager to pause and yeild the control
        # back to the caller to do a particular action/actions
        yield
    finally:
        # Wrap up Code
        obj.obj_attribute -= 1


num_obj = SomeObj(5)
print(num_obj.obj_attribute)
with simple_context_manager(num_obj):
    print(num_obj.obj_attribute)
print(num_obj.obj_attribute)


# Example
from time import time
from contextlib import contextmanager

header = "this is the header content \n"
footer = "\nthis is the footer content \n"

@contextmanager
def new_log_file(file_name):
    try:
        logname = file_name
        file = open(logname, 'w')
        file.wrtie(header)
        yield file
    finally:
        file.write(footer)
        print("Log File Created!!")
        file.close()

with new_log_file('current_logfile') as file:
    file.write("this is the body content")


# Coroutines

REFERENCE = """
Coroutine is build out of Python generator.
It is something you constantly give things to that may or may not return anything.
It takes what is passded to it and does something with it.
What you give it and what it does with it are completely up to you. 

Coroutine is designed to 
    1. Repeatedly send input to it, 
    2. Process that input by following the logical path that you program it to follow, 
    3. and stop when it reaches the yield statement. 

Coroutine object has properties and states that can be referenced and altered. 
Maintaining and using the state is what a coroutine object does. 
It can produce the value and called if needed, but its most important ability is 
    1. to change the state of its own properties, 
    2. the state of something else, 
    3. or both. 

Send() is a method that was added to generators exclusively for the purpose of coroutine functionality. 
In coroutine, the yield statement is used to capture the value of whatever is passed to the send() method. 
In the case of coroutines, the yield statement is not only in charge of pausing the flow, but also capturing values. 
"""

# Coroutine Example 1

def coroutine_example():
    while True:
        x = yield
        # Do something with x
        print(x)

cr_example = coroutine_example()
cr_example.send(10)             # TypeError: can't send non-None value to a just-started generator
# Priming the Coroutine Object by calling next on it - so that it doesn't raise the TypeError
next(cr_example)

# What is happening, is that the value sent to the coroutine is what the yield statement becomes. 
# And since x is set equal to yield [by calling next on it], we can now use x however I want. 
# This is not really obvious if you haven't worked with a coroutine before and can take some getting used to. 
# So just remember that a coroutine has a send method that has a very specific purpose and behavior. 
# It starts at the coroutine where it was last suspended and assigns the parameter key yield. 
# This example will simply print the value.

cr_example.send(10) # returns 10



# Coroutine Example 2

def counter(str_begin):
    count = 0
    try:
        while True:
            # Inputs
            str_test = yield
            if isinstance(str_test, str):
                if str_test in str_begin:
                    count += 1
                    print(str_test)
                else:
                    print('No Match')
            else:
                print('Not a string')
    except GeneratorExit:
        print(count)


# Execution:

c = counter('California')

# Priming the Coroutine
next(c)

# Making Send Calls
c.send('Cali')
c.send('nia')
c.send('India')
c.send(1234)

# Closing the Coroutine
c.close()



# Coroutine Example 3 | Building Coroutine - Decorators

def coroutine_decorator(func):
    def wrap(*args, **kwargs):
        cr = func(*args, **kwargs)
        # Priming the generator - via decorator
        next(cr)
        # returning the coroutine
        return cr
    # returning the wrapped coroutine 
    return wrap


@coroutine_decorator
def coroutine_example():
    while True:
        x = yield
        #do something with x
        print(x)



# Coroutine Example 4 | Coroutine & Decorator

def coroutine_decorator(func):
    def wrap(*args, **kwargs):
        cr = func(*args, **kwargs)
        # Priming the generator - via decorator
        next(cr)
        # returning the coroutine
        return cr
    # returning the wrapped coroutine 
    return wrap

def sender(filename, target):
    for line in open(filename):
        target.send(line)
    target.close()

@coroutine_decorator
def match_counter(str_test):
    count = 0
    try:
        while True:
            line = yield
            if str_test in line:
                count += 1
    except GeneratorExit:
        print('{}: {}'.format(str_test, count))

@coroutine_decorator
def longer_than(n):
    count = 0
    try:
        while True:
            line = yield
            if len(line)>n:
                print(line)
                count += 1
    except GeneratorExit:
        print('longer than {}: {}'.format(n, count))


# Coroutine Example 5 | Coroutine & Decorator

def coroutine_decorator(func):
    def wrap(*args, **kwargs):
        cr = func(*args, **kwargs)
        # Priming the generator - via decorator
        next(cr)
        # returning the coroutine
        return cr
    # returning the wrapped coroutine 
    return wrap


# router coroutine can both send and receive data/values
# router coroutine can branch in more than one direction and send to multiple targets
# takes lines as inputs, split them and then send them to different target
# two targets are instantions of file_write coroutine   

@coroutine_decorator
def router():
    try:
        while True:
            line = yield
            (first, last) = line.split(' ')
            fnames.send(first)
            lnames.send(last.strip())
    except GeneratorExit:
        fnames.close()
        lnames.close()
        
@coroutine_decorator
def file_write(filename):
    try:
        with open(filename,'a') as file:
            while True:
                line = yield
                file.write(line+'\n')
    except GeneratorExit:
        file.close()
        print('one file created')

if __name__ == "__main__":
    fnames = file_write('first_names.txt')
    lnames = file_write('last_names.txt')
    router = router()
    for name in open('names.txt'):
        router.send(name)
    router.close()
        
