version=0.1.5

*** Using IceBrakes ***

Make sure icebrakes.py is executable (use chmod if it isn't)

To run IceBrakes linting on your file simple run 
$ ./icebrakes.py path/to/your/file.py

IceBrakes also supports directories as input and will recursively lint
every python file in a given directory.

You can install IceBrakes with the following command
$ sudo cp icebrakes.py /usr/local/bin/icebrakes

If you are interested in diving into the code or using IceBrakes as a module
I have documented the entire api of icebrakes.py in docs/IceBrakes API.txt


*** What is IceBrakes? ***

IceBreaks is an attempt to provide typescript style const variables to python. That is, 
what if a linter could tell you when you break immutability?

It's true that python has things like tuples and frozen data classes which cannot 
be modified; the value of any variable in python can be freely assigned. Consider the 
following python code.

    x = (1, 2, 3)   # this is a tuple

    x[1] = 7        # TypeError

    x = ()          # VALID PYTHON
    x = (7, 2, 3)   # VALID PYTHON

    x = []          # VALID PYTHON
    x = [7, 2, 3]   # VALID PYTHON

While you cannot change the indivual elements of a tuple there are several other ways 
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
Hashmark dollarsign (#$) as the last two characters of the line tells IceBrakes to 
jump into action. Here's an example use and the expected output, with line numbers for clarity.

    1 def bar():... #$
    2 bar = 56

    > Bad use (foo) was made static on line 1, and mutated on line 2


Once a variable is declared immutable any previous assignments to that name are also 
illegal. See the reverse of the above example.

    1 def foo():...
    2 foo = 56      #$

    > Bad use (foo) was made static on line 2, and mutated on line 1

For more detailed examples of usage read TESTING_README.txt and the unit tests in src/tests/tests

IceBrakes is in early development consisting of less than 100 lines of code, and lots 
and lots of documentation. Now that the docs are written I will focus on adding features 
and more test cases.

Once more features are added you can expect this document to expand and possibly split 
into multiple further documents. If you are looking for more information see docs/manifest.txt
which explains all of the files in IceBrakes.


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


*** Who is the dev? ***

IceBrakes is developed by me, Lars. I'm a linux nerd and Python enthusiast. I'm also a 
musician and in general I like patterns and abstract concepts. 

Permissions are granted to anyone who wishes to use or edit this code in accordance 
with the GPLv3 Copyleft license provided. So you too can be the developer if you'd like.


*** What's in a name? ***

I chose the name IceBrakes because pymmutable was a mouthful. I did try to come up with
other clever names that include py and I felt like it was an uphill battle. I like that ice
implies some level of immutability like a frozen dataclass, and brakes implies that my project
pulls the brakes on your code. Anyways, it's a silly name but it doesn't seem to be taken by 
any other projects so it's the name for now.


*** CONTRIBUTING ***

At the time of publishing IceBrakes will be missing many (most) features
expected of a linter, that is because I have spent a large portion of my time
writing documentation and a testing methodology. I will be developing features
after 0.0.1 launches on github.

Therefore one of the easiest ways to contribute will be to write unit tests for
any missing features so that as I develop the features I can turn the tests on.

If you make a pull request with actual code changes, I will require that you also
include a passing test file (or multiple) formatted according to the project.

Along with a methodology I have also written some tools to make generating and running
tests very very easy. If you are interested in learning more read docs/TESTING_README.txt

Copyright © 2023 Lars S.
