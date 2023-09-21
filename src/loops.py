#!/bin/python3

'''
One of the next major features for icebrakes will be loop awareness
so that an assignment like

while True:
    x = 44   #$

becomes illegal. I will notate all my thoughts and plans for developing
that feature in this scratch file.

I think this will be pretty simple, we need a flag to determine if we are in a loop,
and we handle loop scopes just like function/class scopes. Basically all assignments
to constant inside a loop are illegal. So if we modify some of the state tools to track
loops and exit loops when indentation decreases (these tools already exist for scopes)
then all we need to do is through a loop check anytime a constant is found, and print
a unique message when a constant is found in a loop. That's the entire spice. I could
probably do it in 4-8 line changes total. 

We need a way to track sub loops, my initial thought of a single bool fails because you need
to track how many loops deep you are and what whitespace triggered each loop. Not to different
from the names_in_scope object but without the names. Maybe just the type of loop for/while as
a name then it would look like while.for.while etc. This won't be used as keys but having the
object will be nice for debugging or adding more detailed error messages in the future (unlikely).

When that list of loops is empty we pass the 'not in a loop' test. So that one data object and a
few extra pieces of logic will enable this api.'''
