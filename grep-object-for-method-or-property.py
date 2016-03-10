# These three utilities (uniq_dir, grep, and uniq_grep) are useful for examining
# objects from a debug prompt.

# 'uniq_dir' method returns a list of property/method names that are unique to
# an object, not acquired from its parent.  This cuts out some of the cruft when
# examining an object.

def uniq_dir(o):
    data = list(set(dir(o)) - set(dir(o.aq_parent)))
    return sorted([x for x in data if not '__roles__' in x])

# 'grep' method that takes an object and a term to search for, and prints a
# list of the property and method names that match.  The 'uniq' parameter will
# start with a uniq_dir() list of properties/methods

def grep(o, term, uniq=False):
    if uniq:
        listing = uniq_dir(o)
    else:
        listing = dir(o)
    for k in listing:
        if '__roles__'  in k:
            continue
        if term.lower() in k.lower():
            print k

# Shortcut, rather than passing in the 'uniq' parameter.

def uniq_grep(o, term):
    grep(o, term, uniq=True)


