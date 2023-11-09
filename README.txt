version=0.2.0
######################################################
Development on IceBrakes has paused with version 0.2.0
######################################################

*** Using IceBrakes ***

Make sure icebrakes.py is executable (use chmod if it isn't)

To run IceBrakes linting on your file simple run 
$ ./icebrakes.py path/to/your/file.py

IceBrakes also supports directories as input and will recursively lint
every python file in a given directory.

You can install IceBrakes with the following command
$ sudo cp icebrakes.py /usr/local/bin/icebrakes

If you are interested in diving into the code or using IceBrakes as a module
I have documented the entire api in docs/API.txt


*** What is IceBrakes? ***

IceBreaks is an attempt to provide immutable variables to python. That is, 
what if a linter could tell you when you break immutability?

While it's true that python has things like tuples and frozen data classes which cannot 
be modified unfortunately the value of any variable in a python script can be freely 
assigned. Consider the following python code.

    x = (1, 2, 3)   # this is a tuple

    x[1] = 7        # TypeError

    x = ()          # VALID PYTHON
    x = (7, 2, 3)   # VALID PYTHON

    x = []          # VALID PYTHON
    x = [7, 2, 3]   # VALID PYTHON

While you cannot change the individual elements of a tuple there are several other ways 
to lose track of the value. Here is another example using dataclasses.

    from dataclasses import dataclass

    @dataclass(frozen=True)
    class Foo():
        bar = 0
        car = 1

    foo = Foo()
    foo = False  # VALID PYTHON

Even though our dataclass was frozen, we still lost the data by simply overwriting 
what the name 'foo' references. My proposal is for some kind of syntax to let 
the language know you cannot reassign to a given name.

For simplicity that syntax is implemented as a comment at the end of a line. 
"#S" as the last two characters of the line tells IceBrakes to jump into action.
Here's an example use and the expected output, with line numbers for clarity.

    1 def bar():... #$
    2 bar = 56

    > Bad use (foo) was made static on line 1, and mutated on line 2


Once a variable is declared immutable any previous assignments to that name are also 
illegal. See the reverse of the above example.

    1 def foo():...
    2 foo = 56      #$

    > Bad use (foo) was made static on line 2, and mutated on line 1

For more detailed examples of usage read TESTING_README.txt and the unit tests in src/tests/tests

If you are looking for more information see docs/manifest.txt which explains all of the
files in IceBrakes.


*** Why does IceBrakes exist? ***

I fully realize that the last thing your project needs is another linter. IceBrakes uses pylint, 
mypy and pytest so I am aware how many tools exist, and how little desire I have to add more tools 
and config files to my project.

Why am I writing IceBrakes then? This is my first public project, and I am using it as a chance for me 
to practice documenting and testing a project. Improving my skills as a developer and communicator are 
the primary goals of the IceBrakes project.

IceBrakes also exists as a proof of concept because I am genuinely annoyed by the lack of constant variables
in Python. I really like the way typescript adds that functionality to javascript but I'm not a fan of
needing to compile from one scripting language to another. That is why IceBrakes simply uses comments
in regular valid python files. 

I personally would love to see a "const" keyword added to python but I don't really know how much work
it would be to add something like that to the language so IceBrakes is my stopgap compromise.


Copyright © 2023 Lars S.
