from pelican import signals
import types
import pprint 
import blinker
import inspect
import pelican

def default(name, data):
    print "Entered", name
    pprint.pprint( data)
    
def register():

    # now for a hack
    pelican = inspect.currentframe().f_back.f_locals['self']
    #print pelican.theme


    for x in dir(signals):
        old_fun = signals.__dict__[x]

        
        if isinstance(old_fun, blinker.base.NamedSignal): 
            print "Getting signal", x
            fun = lambda y : default(x,y)
            old_fun.connect( fun )

        #else:
            #print "Skipping", x
            #print type(x)
            #pprint.pprint( old_fun)

        raise Exception("dfsd")
    # now we want to install all the components into the template!
