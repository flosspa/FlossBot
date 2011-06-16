import threading, Queue, os
from Events import *

class Plugin(threading.Thread):
    def __init__(self):
        self.__queue = Queue.Queue(0)
        threading.Thread.__init__(self)
        
    def run(self):
        raise NotImplementedError

    def setNick(self, nick):
        raise NotImplementedError

    def sendToPlugin(self, message):
        self.__queue.put(message)
        
    def getData(self):
        d = None
        try:
            d = self.__queue.get(True, 5)
        except:
            pass
        return d
        
    def setup(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError

    def sendToIrc(self, destination, msg):
        line = "PRIVMSG %s :%s\r\n" % (destination, msg)
        event = Event(IRC_SEND, line)
        getEventManager().signalEvent(event)
        

    def sendToIrcRaw(self, msg):
        event = Event(IRC_SEND, msg)
        getEventManager().signalEvent(event)
    

def find_plugins(path, cls):
    subclasses=[]
    
    def look_for_plugin_classes(modulename):
        module = __import__(modulename)
        
        d=module.__dict__
        for m in modulename.split('.')[1:]:
            d=d[m].__dict__
            
        for key, entry in d.items():
            if key == cls.__name__:
                continue
                
            try:
                if issubclass(entry, cls):
                    subclasses.append(entry)
            except TypeError:
                continue
                
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith(".py") and not name.startswith("__"):
                path = os.path.join(root, name)
                modulename = path.rsplit('.',1)[0].replace('/', '.')
                look_for_plugin_classes(modulename)
                        
    return subclasses



