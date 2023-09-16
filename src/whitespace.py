#!/bin/python3
'''Eventually the functions of this file may get pulled into icebrakes.py, but first I want to
build my algorithms without breaking any of the unit tests.

My original thought process was naive and I assumed I needed to track every white space
change but since I only care about namespaces it's actually a much simpler problem, and
the main engines are already written.

Below I lay out how I will use white_space_parse() from this file along with get_names_from_file()
and paren_parse() from icebrakes.py to solve for namespaces.

Here's the deal with scopes, only the keywords 'def', 'class', 'async def' can
trigger a change in namespace. We don't need to track any other keywords. Words like
'for' and 'if' won't effect this is any way. My original line of thinking considered ternary 
if statements as an edge case but they are not even on my radar anymore.

So what do we really need? A different set of name dicts (constants/all_vars) for each sub 
namespace which will be determined by one of the above keywords and a corresponding white 
space change. We track when the white space goes back to it's original level, and that kills 
the sub namespace.

The good news is we don't need to parse lines more than once, but we need to juggle a lot
more dictionaries. So I need to figure out an api or tool or recursion that allows us to
sub name space for a while and then return out. 

We also either need to parse each set of sub dicts as we are leaving the scope or we need a
dict of all total dicts where the keys are related to the scope that we parse once after reading 
the file. The keys can't be indentation level because two different functions can have the same 
indent level and not be in each other's scopes.

So the name of each function can kind of work as a key but they would need to be sub keyed to their
outer scope, and then everything at the top would be named 'root'.

Here is a python code example.

def foo():
    def bar():
        pass

def bar():
    def foo():
        pass
        
We want to parse than into an object that looks like this.

root.foo
root.foo.bar
root.bar
root.bar.foo

I imagine that is a solved problem in python but it's one I will have to research.

It might be worth implementing some OO for the name dicts. Some struct that contains two
dicts. It will make passing things around a bit easier.

Because I already have paren_parse, I can actually use it to set a flag whenever a new
scope is found, then we unset the flag later by tracking white space. This would basically
mean checking for the sub scope flag (or int?) every pass and then carefully tracking white
space when it is set. This will have a huge time deficit but I always knew that.

The reason I think we need an int instead of a bool for a flag is to track how many sub scopes
deep we are. So 0 means root and 1 means one function def in, etc. Then every time we leave a scope,
we subtract one, and once the number is 0 we're not in a scope anymore. This will work with a nice
'if flag:' check because 0 is already falsey.

In get_names_from_file() is where I should track white space and check flags. I need to count 
the whitespace before stripping it, and move left/right accordingly. 

Things are structured and functional enough now that I think I can achieve this change with
only one or two additional functions. My next step will be to write out what those functions
might look like, and then I will try building that engine. When this step is complete most of 
the rest of the unit tests can be turned on because a large amount of them relate to white space.

I will also need a new major feature to work towards (loops) but I'm sure something will come up.
'''

from math import gcd
from functools import reduce
from typing import Set


def white_space_parse(file: str) -> int:
    '''Takes a file, calculates the indentation level using magic.
    For now we parse the first 100 lines of the file as that should be more than enough,
    but that number can probably be reduced a bit. It doesn't start counting until white
    space is found which ignores imports/doc strings in the line count.

    Also we are considering tabs as whitespace but there will be more work to process them
    later (aka you are a monster if your file has tabs in it), and also it's gonna be a mess 
    if you mix whitespace/tabs. So IceBrakes is going to assume some level of responsibility 
    belongs with the dev.
    
    I was kind of surprised I couldn't find a package or tool to do this since python is all about
    indentation levels but it turned out to be a really easy solve. 
    '''

    levels: Set = set()
    with open(file, encoding="UTF-8") as tempfile:
        num: int = 0
        for line in tempfile:
            if num == 100:
                break
            if line[0] in "\t ":
                len_line_lstrip = len(line.lstrip())

                # This removes any lines that only have whitespace on them
                # Of course so should your other linter but you know.
                if len_line_lstrip > 0:
                    num += 1
                    size = len(line) - len_line_lstrip
                    levels.add(size)
    if levels:
        # tnt here is also for mypy
        return int(reduce(gcd, levels))

    # This is just for mypy/pylint
    return 1

#out = white_space_parse('icebrakes.py')
#print(out)
