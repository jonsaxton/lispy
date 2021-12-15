import sys, lispio
sxp   = lispio.putSexp # function to convert python list to Sexp
debug = False          # show trace of evaluations if true
Alist = []             # Hold the global defs

def isSymbol(x) : return type(x) == type('') 
def isNumber(x) : return type(x) == type(0.0) 

def pairlis (x,y,alist) :
    """push symbols in x with respective values in y onto the alist"""
    if not x : return alist
    else : return [[x[0],y[0]]] + pairlis(x[1:],y[1:],alist)
 
def assoc (x, alist) :
    "look up x on the alist and return its value"
    if   not alist        : return []    # nil
    elif alist[0][0] == x : return alist[0][1]
    else                  : return assoc(x,alist[1:])
 
def apply (fn,args,alist) :
    "apply a function fn to its arguments in args"
    if debug :
        print("--Apply-- %s  Args=%s" % (sxp(fn),sxp(args)))
        printAlist(alist)

    if isSymbol(fn) :   # name of a function
        if   fn == 'atom' : return [[],'t'][type(args[0]) != type([])]
        elif fn == 'car'  : return args[0][0]   # first element of 1st arg
        elif fn == 'cdr'  : return args[0][1:]  # tail of 1st arg
        elif fn == '+'    : return args[0]+args[1]
        elif fn == '-'    : return args[0]-args[1]
        elif fn == '*'    : return args[0]*args[1]
        elif fn == '/'    : return args[0]/args[1]
        elif fn == 'eq'   : return [[],'t'][args[0] == args[1]]
        elif fn == 'not'  : return [[],'t'][args[0] == []]
        elif fn == 'cons' :
            if type(args[1]) != type([]) : args[1] = [args[1]]
            return [args[0]] + args[1]
        else : return (apply(eval(fn,alist),args,alist))
    elif fn[0] == 'lambda' : # a function definition
        return eval (fn[2], pairlis(fn[1],args,alist))
    else                   : scream("Can't apply %s" % fn)

def eval (exp, alist) :
    "evaluate an S expression using the alist"
    global Alist
    if debug : print("--Eval--- %s" %  sxp(exp)); printAlist(alist)
    if   exp == 't'     : return 't'      # true evaluates to itself
    elif exp == 'nil'   : return []       # symbol nil same as a null list
    elif exp == 'alist' : return Alist    # special command to examine alist
    elif isNumber(exp)  : return exp      # numbers eval to themselves
    elif isSymbol(exp)  : return assoc(exp,alist)  # look up variables
    else :               # check for special forms
        if   exp[0] == 'quote' : return exp[1]
        elif exp[0] == 'def' :            # user define functions
            alist = Alist = pairlis([exp[1]],[exp[2]],alist)
            return exp[1]                 # return function name
        elif exp[0] == 'cond'  : return evcon(exp[1:], alist)
        else :
            x = evlis(exp[1:], alist)
            return apply (exp[0],x , alist)

def evcon (c, alist) :
    "evaluate cond. Note just the pairs passed in c"
    if   len(c) == 0           : return []
    elif eval (c[0][0], alist) : return eval (c[0][1],alist)
    else                       : return evcon(c[1:],  alist)

def evlis (l, alist) :
    "evaluate all elements in a list, returning list of the values"
    if not l : return []
    else     : return [eval(l[0], alist)] + evlis(l[1:], alist)

def printAlist(alist) :
    print ("Alist")
    for pair in alist :
        name,sexp = pair
        sexp = sxp(sexp)
        output = "(%s %s)" % (name,sexp)
        if len(output) > 50 : output = output[:50]+"..."
        print(output)

def scream(mesg) :
    print("Exiting: %s" % mesg)
    sys.exit(1)

def main () :   
    "get S expressions and evaluate them. Print the results"
    global Alist, debug
    while True :
        s = lispio.getSexp()
        if   s == 'alist' : printAlist(Alist)
        elif s == 'debug' : debug = not debug
        else :
            try    : print(lispio.putSexp(eval(s ,Alist)))
            except : scream("cant eval %s " % s)

if __name__ == "__main__" : main()
