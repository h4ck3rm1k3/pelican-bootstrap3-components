from pelican import signals
import types
import pprint 
import blinker
import inspect
import pelican
import six 
import logging
import sys
logger = logging.getLogger(__name__)

def default(name, data):
    print "Entered", name
    pprint.pprint( data)
    
def import_component(pelican,plugin):

    logger.debug('Temporarily adding PLUGIN_PATHS to system path')
    _sys_path = sys.path[:]
    for pluginpath in pelican.settings['BOOTSTRAP_COMPONENTS_PATHS']:
        sys.path.insert(0, pluginpath)
        logger.debug("Sys path now %s" % sys.path)

    #logger.debug("Sys path now %s" % sys.path)
    #print ("Sys path now %s" % sys.path)

    # taken from pelican.init_plugins
    # if it's a string, then import it
    if isinstance(plugin, six.string_types):
        logger.debug("Loading plugin `%s`", plugin)
        try:
            plugin = __import__(plugin, globals(), locals(),
                                str('module'))
        except ImportError as e:
            logger.error(
                "Cannot load plugin `%s`\n%s", plugin, e)
            return

    logger.debug("Registering plugin `%s`", plugin.__name__)
    plugin.register(pelican)
    pelican.bootstrap_components.append(plugin)

def get_generators(pel):
    generators = []
    print 'get generators'
    #pprint.pprint(x)
    for x in pel.bootstrap_components :
        generators.append(x.get_generators(pel))
    return generators

custom_signals = { 'get_generators': get_generators }

def register():

    print 'register'
    # now for a hack
    pelican = inspect.currentframe().f_back.f_locals['self']
    #print pelican.theme

    pelican.bootstrap_components=[]

    comps = pelican.settings['BOOTSTRAP_COMPONENTS']
    for c in comps:
        import_component(pelican,c)

    for x in dir(signals):
        old_fun = signals.__dict__[x]
        
        if isinstance(old_fun, blinker.base.NamedSignal): 
            
            if x in custom_signals:
                print "Getting signal", x
                fun = custom_signals[x]
                old_fun.connect( fun )
                
            else:

                print "custom signal", x
                fun = lambda y : default(x,y)
                old_fun.connect( fun )

