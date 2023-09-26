#!/bin/python3
'''
For single line strings we only need to worry about equal line parse
and I think it might be abstractly simple in that we only care if ' or "
occur before the equal sign.

'word' = 5   # illegal

This going to be implemented in the same way I originally approached skipping
parenthesis before I wrote paren_parser (which could use a new name).

I'm also going to add that feature back in to avoid lines like this

foo(bar=55)
since that should be allowed. 

These changes will take place exclusively in equal_sign_parse() and I
will also change the order of equal_sign_parse() and paren_parse() assuming
that doesn't break any tests.
'''
