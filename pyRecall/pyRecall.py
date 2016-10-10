'''Main for pyRecall'''
import hashlib
import pickle
import os
import inspect
import shutil

def pyRecall(func, verbose=False):
    '''Decorator to print function call details - parameters names and effective values'''

    def checkExistenceOfPyRecallFolder():
        return os.path.exists(".pyRecall")
        
    def pickleFile(func_name, hash_val):
        '''Return string with path and file name of the pickle'''
        return ".pyRecall/"+func_name+"_"+hash_val+".p"

    def checkWhetherPickleExists(func_name, hash_val):
        fname = pickleFile(func_name, hash_val)
        return os.path.exists(fname)

    def loadPickle(func_name, hash_val):
        fname = pickleFile(func_name, hash_val)
        return pickle.load(open(fname, "rb"))

    def dumpPickle(func_name, func_return, hash_val):
        fname = pickleFile(func_name, hash_val)
        pickle.dump(func_return, open(fname, "wb"))

    def wrapper(*func_args, **func_kwargs):
        arg_names = func.__code__.co_varnames[:func.__code__.co_argcount]
        args = func_args[:len(arg_names)]
        defaults = func.__defaults__ or ()
        args = args + defaults[len(defaults) - (func.__code__.co_argcount - len(args)):]
        params = list(zip(arg_names, args))
        args = func_args[len(arg_names):]
        if args:
            params.append(('args', args))
        if func_kwargs:
            params.append(('kwargs', func_kwargs))
        arg_string = func.__name__ + ' (' + ', '.join('%s = %r' % p for p in params) + ' )'
        #print(arg_string)

        func_code = inspect.getsourcelines(func)

        #Pack function arguments and function code into a list
        toBeHashed = [arg_string, func_code]
        #print(func_code)
        func_name = func_code[0][1].split(' ')[1].split('()')[0]
        z = pickle.dumps(toBeHashed)
        hash_val = hashlib.md5(z).hexdigest()
        #print(hash_val)

        if checkExistenceOfPyRecallFolder() == False:
            os.mkdir('.pyRecall')

        if checkWhetherPickleExists(func_name, hash_val) == True:
            func_return = loadPickle(func_name, hash_val)
        else:
            func_return = func(*func_args, **func_kwargs)
            dumpPickle(func_name, func_return, hash_val)

        return func_return
    return wrapper



def forgetRecalls():
    '''Remove pre-existing funcRecall archive'''
    try:
        shutil.rmtree('.pyRecall')
    except:
        print('Nothing to forget')
