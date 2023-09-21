#!/bin/python3

'''This file is where I will think out and plan string awareness
for icebrakes. Icebrakes needs to know that lines like this
"foo = 44 " are not an assignment. 

I will have to take nested strings into account.  (DO I?)

Here is how I see the string problem. Multi line strings are the biggest deal
because they invalidate entire lines. So I need some kind of flag that
sets a multiline string, and we just skip every line until that flag is unset. 

We don't need the names from those lines but we do care about parsing for the 
three quote mark pattern to end the multiline string.

As for single line strings we only need to worry about equal line parse
and I think it might be abstractly simple in that we only char if ' or "
occur before the equal sign.

'word' = 5   # illegal

That's invalid python anyways, mostly for assignment the equal sign goes left
so single strings might be a very simple task. (for the purposes of this linter)

These two modes are basically entirely different parts of the code I need to edit
and so it might make sense to do it in two patches. Idk I kind of want to avoid
a weird string limbo where things half work.

I need a few vars to track the beginning and ended of every """ triple quote.
Or maybe only the outermost triple quote at a time. This """ doesn't mean
anything to python because it's already a string.

I guess we need to check every line for triple quotes and when we are in a multi
line string we need the leftmost match. We also care if a trip quote appears twice
is the same line so we actually need to parse the entire line.'''
