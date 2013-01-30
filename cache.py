import sqlite3
import os
import multiprocessing

class Cache:
    def __init__(self, filename, reset=False, datatype='TEXT', lock=multiprocessing.RLock()):
        '''
        Create a new cache for working data
        By default uses a multiprocessing lock, if you are just multithreading, you could pass in a multithreading lock
        By default, does not wipe out old cache - this can be overridden in case of a crash or for debugging.
        a 'datatype' argument can also be passed to say what kind of datatype you want to use in the sql table
        '''
        with lock:
            new_db = True
            if os.path.exists(filename):
                if reset:
                    os.remove(filename)
                else:
                    new_db = False
                
            self.filename = filename
            self.connect()
            if new_db:
                self.cursor.execute('CREATE TABLE cache (key TEXT PRIMARY KEY, value %s)' % datatype)
            self.connection.commit()
            self.disconnect()
            self.lock = lock
        
    def connect(self):
        self.connection = sqlite3.connect(self.filename)
        self.cursor = self.connection.cursor()
    def disconnect(self):
        self.cursor.close()
        self.connection.close()
    
    def wipe(value=0):
        '''
        remove all items with a value matching value, default is 0
        '''
        with self.lock:
            self.connect()
            self.cursor.execute('DELETE FROM cache WHERE value = ?', (value,))
            self.cursor.commit()
            self.disconnect()
        
        
    def put(self, key, value):
        '''
        Put something into the cache, replacing the old value if there was one
        '''
        with self.lock:
            self.connect()
            cursor = self.cursor
            cursor.execute('REPLACE INTO cache (key, value) VALUES (?,?)', (key, value))
            self.connection.commit()
            #self.writes.value += 1
            #if self.writes.value >= self.writes_before_commit:
            #    self.writes.value = 0
            #    self.connection.commit()
            self.disconnect()
    
    def __contains__(self, item):
        '''
        check if a key is in the cache
        '''
        with self.lock:
            self.connect()
            self.cursor.execute("SELECT key FROM cache WHERE key = ?", (item,))
            if len(self.cursor.fetchall()) > 0:
                self.disconnect()
                return True
            else:
                self.disconnect()
                return False
            
    def contains(self, item):
        return self.__contains__(item)
    
    def get(self, key):
        '''
        get a value
        '''
        with self.lock:
            self.connect()
            self.cursor.execute('SELECT value FROM cache WHERE key = ?', (item,))
            rows = self.cursor.fetchall()
            self.disconnect()
            if len(rows) == 0:
                return None
            else:
                return rows[0][0]
    
    