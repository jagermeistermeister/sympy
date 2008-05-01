import py
from sympy import Symbol, sin, cos, Rational, sqrt, exp, sinh, cosh, tanh, \
        coth, asinh, acosh, atanh, acoth, pi, I, log
from sympy.utilities.pytest import XFAIL
from sympy import O
#from sympy.core.power import pole_error

def test_bug5():
    x = Symbol("x", real=True)
    w = Symbol("w", real=True)
    e = w**(1-log(x)/(log(2) + log(x)))
    f = e.series(w,0,1)
    e = sin(2*w)/w
    f = e.series(w,0,2)
    # this fails if real=False for x and w, due to a caching bug in Order
    assert f == 2 + O(w**2)

def testseries1():
    x = Symbol("x")
    e = sin(x)
    assert e.series(x,0,0) != 0
    assert e.series(x,0,0) == O(1, x)
    assert e.series(x,0,1) == O(x, x)
    assert e.series(x,0,2) == x + O(x**2, x)
    assert e.series(x,0,3) == x + O(x**3, x)
    assert e.series(x,0,4) == x-x**3/6 + O(x**4, x)

    e = (exp(x)-1)/x
    assert e.series(x,0,2) == 1+x/2+O(x**2, x)
    #this tests, that the Basic.series() cannot do it (but Mul.series can)
    #py.test.raises(g.core.power.pole_error, g.core.basic.Basic.series, e,x,0)

    assert x.series(x,0,0) == O(1, x)
    assert x.series(x,0,1) == O(x, x)
    assert x.series(x,0,2) == x

def testseriesbug1():
    x = Symbol("x")
    assert (1/x).series(x,0,3) == 1/x
    assert (x+1/x).series(x,0,3) == x+1/x

def testseries2():
    x = Symbol("x")
    assert ((x+1)**(-2)).series(x,0,4) == 1-2*x+3*x**2-4*x**3+O(x**4, x)
    assert ((x+1)**(-1)).series(x,0,4) == 1-x+x**2-x**3+O(x**4, x)
    assert ((x+1)**0).series(x,0,3) == 1
    assert ((x+1)**1).series(x,0,3) == 1+x
    assert ((x+1)**2).series(x,0,3) == 1+2*x+x**2+O(x**3, x)
    assert ((x+1)**3).series(x,0,3) == 1+3*x+3*x**2+O(x**3, x)

    assert (1/(1+x)).series(x,0,4) == 1-x+x**2-x**3+O(x**4, x)
    assert (x+3/(1+2*x)).series(x,0,4) == 3-5*x+12*x**2-24*x**3+O(x**4, x)

    assert ((1/x+1)**3).series(x,0,3)== 1+x**(-3)+3*x**(-2)+3/x+O(x**3, x)
    assert (1/(1+1/x)).series(x,0,4) == x-x**2+x**3-O(x**4, x)
    assert (1/(1+1/x**2)).series(x,0,6) == x**2-x**4+O(x**6, x)

@XFAIL
def testfind():
    # XXX find() doesn't exist
    a = Symbol("a")
    b = Symbol("b")
    c = Symbol("c")
    p = Rational(5)
    e = a*b+b**p
    assert e.find(b)
    assert not e.find(c)

def xtest_log():
    "too difficult"
    x = Symbol("x")
    ec = exp(Rational(1))
    e = (log(1/x+ec)-ec) / (x*log(1/x+1))
    d = e.diff(x)

def xtest_bug2(): ### 1/log(0) * log(0) problem
    w = Symbol("w")
    e = (w**(-1)+w**(-log(3)*log(2)**(-1)))**(-1)*(3*w**(-log(3)*log(2)**(-1))+2*w**(-1))
    e = e.expand()
    #should be 3, but is 2
    assert e.series(w,0,4).subs(w,0)==3

def test_exp():
    x = Symbol("x")
    e = (1+x)**(1/x)
    assert e.series(x,0,2) == exp(1) - x*exp(1)/2 + O(x**2, x)

def test_exp2():
    x = Symbol("x", real=True)
    w = Symbol("w", real=True)
    e = w**(1-log(x)/(log(2) + log(x)))
    assert e.series(w,0,1) != 0

def test_bug3():
    x = Symbol("x")
    e = (2/x+3/x**2)/(1/x+1/x**2)
    assert e.series(x,0,1) == 3+O(x)

def test_generalexponent():
    x = Symbol("x")
    p = 2
    e = (2/x+3/x**p)/(1/x+1/x**p)
    assert e.series(x,0,1).leadterm(x) == (3,0)
    p = Rational(1,2)
    e = (2/x+3/x**p)/(1/x+1/x**p)
    assert e.series(x,0,1).leadterm(x) == (2,0)

    e=1+x**Rational(1,2)
    assert e.series(x,0,4) == 1+x**Rational(1,2)

# more complicated example
def test_genexp_x():
    x = Symbol("x")
    e=1/(1+x**Rational(1,2))
    assert e.series(x,0,2) == \
                1+x-x**Rational(1,2)-x**Rational(3,2)+O(x**2, x)

# more complicated example
def test_genexp_x2():
    x = Symbol("x")
    p = Rational(3,2)
    e = (2/x+3/x**p)/(1/x+1/x**p)
    assert e.series(x,0,1).leadterm(x) == (3,0)

@XFAIL
def test_subsbug1():
    # XXX pole_error doesn't exist
    x = Symbol("x")
    e = 1 + x**Rational(1,2)
    e = e.diff(x)
    py.test.raises(g.core.power.pole_error, e.subs, x, Rational(0))

def test_seriesbug2():
    w = Symbol("w")
    #simple case (1):
    e = ((2*w)/w)**(1+w)
    assert e.series(w,0,1) == 2 + O(w, w)
    assert e.series(w,0,1).subs(w,0) == 2

    #test sin
    e = sin(2*w)/w
    assert e.series(w,0,2) == 2 + O(w**2, w)

    #more complicated case, but sin(x)~x, so the result is the same as in (1)
    e=(sin(2*w)/w)**(1+w)
    assert e.series(w,0,1) == 2 + O(w)
    assert e.series(w,0,3) == 2-Rational(4,3)*w**2+w**2*log(2)**2+2*w*log(2)+O(w**3, w)
    assert e.series(w,0,2).subs(w,0) == 2

@XFAIL
def test_seriesbug3():
    # XXX Fails with infinte recursion
    x = Symbol("x")
    w = Symbol("w")

    #some limits need this series expansion to work:
    e = (w**(-log(5)/log(3))-1/w)**(1/x)
    assert e.series(w,0,1).subs(log(w),-log(3)*x).subs(w,0) == 5

def test_order():
    #these tests basically define the O's behavior. So be very careful
    #when changing them (as with every test in SymPy :)
    x = Symbol("x")
    assert O(x) == O(x)
    assert O(x**2) == O(x**2)
    assert O(x) != O(x**2)

    assert O(x) + O(x) == O(x)
    assert O(x) - O(x) == O(x)

    assert O(2*x) == O(x)
    assert 2*O(x) == O(x)
    assert O(3*x) == O(x)
    assert 3*O(x) == O(x)
    assert O(x) == O(x*8)
    assert O(x) == O(x)*8

    assert O(x+1) == O(1,x)
    assert O(x)+0 == O(x)
    assert O(x)+0 == 0+O(x)
    assert O(x)+1 != O(x)
    assert O(x)+1 == 1+O(x)
    assert O(x)+x == O(x)
    assert O(x)+x**2 == O(x)
    assert O(x)+x**3 == O(x)

    assert x*O(x) == O(x**2)
    assert O(x)*x == O(x**2)
    assert O(x**3)*x == O(x**4)

    assert ((x+O(x)) - (x+O(x))) == O(x)
    assert O(x)/x == O(1,x)

    assert O(x)*O(x) == O(x**2)

    # XXX these three fail
    #assert O(1,x).diff(x) == O(1,x)
    #assert O(x).diff(x) == O(1,x)
    #assert O(x**2).diff(x) == O(x)

    assert O(x)*Symbol("m") == O(x)
    a = Rational(1,3)+x**(-2)+O(x)
    b = Rational(1,6)-x**(-2)+O(x)
    assert a+b == Rational(1,2) + O(x)

    x = Symbol("w")
    assert O(x)+1 != O(x)

    assert (2+O(x)) != 2
    # XXX These two fail because removeO is not a method
    #assert (2+O(x)).removeO() == 2
    #assert (2+x+O(x**2)).removeO() == x+2

def test_order_bug():
    x = Symbol("x")
    a = -4
    b = -3/x
    e1 = O(x)*a+O(x)*b
    e2 = O(x)*(a+b)
    assert e1 == O(1,x)
    assert e1 == e2

    assert O(x**2)*(1+2/x+3/x**2) == O(1,x)
    assert O(1+2/x+3/x**2) == O(1/x**2)

def test_order_expand_bug():
    x = Symbol("x")

    assert O(x**2)+x+O(x) == O(x)
    a = O(x**2) + 2*x
    b = 3+O(x)
    assert a+b == 3+O(x)

    e = (2/x+3*x**(-2))*(O(x**3)+x**2)
    assert e.expand() == 3 + O(x)

@XFAIL
def test_expbug4():
    # XXX O(x).series not implemented
    x = Symbol("x")
    assert (log(sin(2*x)/x)*(1+x)).series(x,0,2) == log(2) + x*log(2) + O(x**2, x)
    assert exp(log(2)+O(x)).series(x,0,2) == 2 +O(x**2, x)
    assert exp(log(sin(2*x)/x)*(1+x)).series(x,0,2) == 2 + O(x**2, x)
    assert ((2+O(x))**(1+x)).series(x,0,2) == 2 + O(x**2, x)

def test_logbug4():
    # XXX O(x).series not implemented
    x = Symbol("x")
    assert log(2+O(x)).series(x,0,2) == log(2) + O(x, x)

@XFAIL
def test_expbug5():
    # XXX O(x).series not implemented
    x = Symbol("x")
    assert exp(O(x)).series(x,0,2) == 1 + O(x**2, x)
    assert exp(log(1+x)/x).series(x,0,2) == exp(1) + O(x, x)

def test_sinsinbug():
    x = Symbol("x")
    assert sin(sin(x)).series(x,0,8) == x-x**3/3+x**5/10-8*x**7/315+O(x**8)

def test_issue159():
    x = Symbol("x")
    a=x/(exp(x)-1)
    assert a.series(x,0,5) == 1 - x/2 - x**4/720 + x**2/12 + O(x**5)

def test_issue105():
    x = Symbol("x")
    f = sin(x**3)**Rational(1,3)
    assert f.series(x,0,17) == x - x**7/18 - x**13/3240 + O(x**17)

def test_issue125():
    y = Symbol("y")
    f=(1-y**(Rational(1)/2))**(Rational(1)/2)
    assert f.series(y,0,2) == 1 - sqrt(y)/2-y/8-y**Rational(3,2)/16+O(y**2)

def test_issue364():
    w = Symbol("w")
    x = Symbol("x")
    e = 1/x*(-log(w**(1 + 1/log(3)*log(5))) + log(w + w**(1/log(3)*log(5))))
    assert e.series(w,0,0) == log(w)/x - log(w**(1 + log(5)/log(3)))/x + O(1,w)

def test_sin():
    x = Symbol("x")
    y = Symbol("y")
    assert sin(8*x).series(x, 0, 4) == 8*x - 256*x**3/3 + O(x**4)
    assert sin(x+y).series(x, 0, 1) == sin(y) + O(x)
    assert sin(x+y).series(x, 0, 2) == sin(y) + cos(y)*x + O(x**2)
    assert sin(x+y).series(x, 0, 5) == sin(y) + cos(y)*x - sin(y)*x**2/2 - \
        cos(y)*x**3/6 + sin(y)*x**4/24 + O(x**5)

def test_issue416():
    x = Symbol("x")
    e = sin(8*x)/x
    assert e.series(x, 0, 5) == 8 - 256*x**2/3 + 4096*x**4/15 + O(x**5)

def test_issue406():
    x = Symbol("x")
    e = sin(x)**(-4)*(cos(x)**Rational(1,2)*sin(x)**2 - \
            cos(x)**Rational(1,3)*sin(x)**2)
    assert e.series(x, 0, 5) == -Rational(1)/12 - 7*x**2/288 - \
            43*x**4/10368 + O(x**5)

def test_issue402():
    x = Symbol("x")
    a = Symbol("a")
    e = x**(-2)*(x*sin(a + x) - x*sin(a))
    assert e.series(x, 0, 4) == cos(a) - sin(a)*x/2 - cos(a)*x**2/6 + \
            sin(a)*x**3/24 + O(x**4)
    e = x**(-2)*(x*cos(a + x) - x*cos(a))
    assert e.series(x, 0, 4) == -sin(a) - cos(a)*x/2 + sin(a)*x**2/6 + \
            cos(a)*x**3/24 + O(x**4)

def test_issue403():
    x = Symbol("x")
    e = sin(5*x)/sin(2*x)
    assert e.series(x, 0, 5) == Rational(5,2) - 35*x**2/4 + 329*x**4/48 + O(x**5)

def test_issue404():
    x = Symbol("x")
    e = sin(2 + x)/(2 + x)
    assert e.series(x, 0, 2) == sin(2)/2 + x*cos(2)/2 - x*sin(2)/4 + O(x**2)

def test_issue407():
    x = Symbol("x")
    e = (x + sin(3*x))**(-2)*(x*(x + sin(3*x)) - (x + sin(3*x))*sin(2*x))
    assert e.series(x, 0, 5) == -Rational(1,4) + 5*x**2/96 + 91*x**4/768 + O(x**5)

#unfortunately, it sometimes fails, due to other bugs and caching:
@XFAIL
def test_issue409():
    x = Symbol("x")
    assert log(sin(x)).series(x, 0, 5) == log(x) - x**2/6 - x**4/180 + O(x**5)
    e = -log(x) + x*(-log(x) + log(sin(2*x))) + log(sin(2*x))
    assert e.series(x, 0, 5) == log(2)+log(2)*x-2*x**2/3-2*x**3/3-4*x**4/45+O(x**5)

def test_issue408():
    x = Symbol("x")
    e = x**(-4)*(x**2 - x**2*cos(x)**Rational(1,2))
    assert e.series(x, 0, 5) == Rational(1,4) + x**2/96 + 19*x**4/5760 + O(x**5)

def test_issue540():
    x = Symbol("x")
    assert sin(cos(x)).series(x, 0, 5) == sin(1) -x**2*cos(1)/2 - x**4*sin(1)/8 + x**4*cos(1)/24 + O(x**5)

def test_hyperbolic():
    x = Symbol("x")
    assert sinh(x).series(x, 0, 6) == x + x**3/6 + x**5/120 + O(x**6)
    assert cosh(x).series(x, 0, 5) == 1 + x**2/2 + x**4/24 + O(x**5)
    assert tanh(x).series(x, 0, 6) == x - x**3/3 + 2*x**5/15 + O(x**6)
    assert coth(x).series(x, 0, 6) == 1/x - x**3/45 + x/3 + 2*x**5/945 + O(x**6)
    assert asinh(x).series(x, 0, 6) == x - x**3/6 + 3*x**5/40 + O(x**6)
    assert acosh(x).series(x, 0, 6) == pi*I/2 - I*x - 3*I*x**5/40 - I*x**3/6 + O(x**6)
    assert atanh(x).series(x, 0, 6) == x + x**3/3 + x**5/5 + O(x**6)
    assert acoth(x).series(x, 0, 6) == x + x**3/3 + x**5/5 + pi*I/2 + O(x**6)

#this only works sometimes (caching problems)
@XFAIL
def test_series2():
    w = Symbol("w")
    x = Symbol("x")
    e =  w**(-2)*(w*exp(1/x - w) - w*exp(1/x))
    assert e.series(w, 2) == -exp(1/x) + w * exp(1/x) / 2  + O(w**2)

#this only works sometimes (caching problems)
@XFAIL
def test_series3():
    w = Symbol("w")
    x = Symbol("x")
    e = w**(-6)*(w**3*tan(w) - w**3*sin(w))
    assert e.series(w, 2) == Integer(1)/2 + O(w**2)
