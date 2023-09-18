# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming

from goody import type_as_str
import inspect


class Check_All_OK:
    """
    Check_All_OK class implements __check_annotation__ by checking whether each
      annotation passed to its constructor is OK; the first one that
      fails (by raising AssertionError) prints its problem, with a list of all
      annotations being tried at the end of the check_history.
    """
       
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_All_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check,param,value,check_history):
        for annot in self._annotations:
            check(param, annot, value, check_history+'Check_All_OK check: '+str(annot)+' while trying: '+str(self)+'\n')

class Check_Any_OK:
    """
    Check_Any_OK implements __check_annotation__ by checking whether at least
      one of the annotations passed to its constructor is OK; if all fail 
      (by raising AssertionError) this classes raises AssertionError and prints
      its failure, along with a list of all annotations tried followed by the
      check_history.
    """
    
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_Any_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check,param,value,check_history):
        failed = 0
        for annot in self._annotations: 
            try:
                check(param, annot, value, check_history)
            except AssertionError:
                failed += 1
        if failed == len(self._annotations):
            assert False, repr(param)+' failed annotation check(Check_Any_OK): value = '+repr(value)+\
                         '\n  tried '+str(self)+'\n'+check_history                 

class Check_Annotation:
    # We start by binding the class attribute to True meaning checking can occur
    #   (but only when the function's self._checking_on is also bound to True)
    checking_on  = True
  
    # For checking the decorated function, bind its self._checking_on as True
    def __init__(self, f):
        self._f = f
        self._checking_on = True

    # Check whether param's annot is correct for value, adding to check_history
    #    if recurs; defines many local function which use it parameters.  
    def check(self,param,annot,value,check_history=''):


        def check_list(par, ano, val):
            assert isinstance(val,list), f"\'{par}\' failed annotation check(wrong type): value = {val} was type {type(val).__name__} ...should be type {ano}"
            
            if len(ano) == 1:
                for v in val:
                    self.check(par, ano[0], v)

            elif type(ano[0]) in [tuple, list, set, dict]:
                for v in val:
                    self.check(par,ano[0],v)
                    
         
            else:
                for i in range(len(ano)):
                    try:
                        if type(val[i]) != ano[i]:
                            raise AssertionError(f"\'{par}\' failed annotation check(wrong type): value = {val[i]} was type {type(val[i]).__name__} ...should be type {ano[i].__name__} list[{i}] check: {ano[i]}")
                    except IndexError: 
                        raise AssertionError(f"\'{par}\' failed annotation check(wrong number of elements): value = {val} annotation had {len(ano)} elements {ano}")
                    except:
                        raise AssertionError(f"\'{par}\' failed annotation check(wrong type): value = {val[i]} was type {type(val[i]).__name__} ...should be type {ano[i].__name__} \n\tlist[{i}] check: {ano[i]}")
                
                    
        def check_tuple(par,ano, val):
            assert isinstance(val,tuple), f"\'{par}\' failed annotation check(wrong type): value = {val} was type {type(val).__name__} ...should be type {ano}"  
            if len(ano) == 1 and (type(ano[0]) not in [tuple, list, set, dict]):
                try:
                    for v in val:
                        if not isinstance(v,ano[0]):
                            raise AssertionError(f"\'{par}\' failed annotation check(wrong type): value = {v} was type {type(v).__name__} ...should be type {ano[0].__name__}")
                except TypeError:
                    raise AssertionError(f"\'{par}\' failed annotation check(wrong number of elements): value = {v} annotation had {len(ano)} elements {ano}")
                
            elif type(ano[0]) in [tuple, list, set, dict]:
                for v in val:
                    self.check(par,ano[0],v)
            else:
                for i in range(len(ano)):
                    try:
                        if not isinstance(val[i],ano[i]):
                            raise AssertionError(f"\'{par}\' failed annotation check(wrong type): value = {val[i]} was type {type(val[i]).__name__} ...should be type {ano[i].__name__}")
                    except IndexError: 
                        raise AssertionError(f"\'{par}\' failed annotation check(wrong number of elements): value = {val} annotation had {len(ano)} elements {ano}")
                    except:
                        raise AssertionError(f"\'{par}\' failed annotation check(wrong type): value = {val[i]} was type {type(val[i]).__name__} ...should be type {ano[i].__name__}")
                
        
        def check_dict(par,ano, val):
            assert isinstance(ano,dict), f"\'{par}\' failed annotation check(wrong type): value = {val} was type {type(val).__name__} ...should be type {type(ano).__name__}"
            assert isinstance(val,dict), f"\'{par}\' failed annotation check(wrong type): value = {val} was type {type(val).__name__} ...should be type {type(ano).__name__}"

            if len(val) < len(ano):
                raise AssertionError(f"\'{par}\' annotation inconsistency: {type(val).__name__}, should have {len(ano)} item but had {len(val)}")
            
            for k,v in ano.items():
                for key, value in val.items():
                        self.check(par, k, key)
                        self.check(par, v, value)
                        
            
            
            
        def check_set(par,ano, val):
            if len(ano) > 1:
                raise AssertionError(f"\'{par}\' annotation inconsistency: set should have 1 value but had {len(ano)} annotation = {ano}")
            
            
            assert isinstance(val,set), f"\'{par}\' failed annotation check(wrong type): value = {val} was type {type(val).__name__} ...should be type {type(ano).__name__}"
            
            for v in val:
                if not isinstance(v,list(ano)[0]):
                    raise AssertionError(f"\'{par}\' failed annotation check(wrong type): value = {v} was type {type(v).__name__} ...should be type {type(ano[0]).__name__}")
            
            
            
        
        def check_frozenset(par, ano, val):
            assert isinstance(val,frozenset), f"\'{par}\' failed annotation check(wrong type): value = {val} was type {type(val).__name__} ...should be type {type(ano).__name__}"
            assert isinstance(ano,frozenset), f"\'{par}\' failed annotation check(wrong type): value = {val} was type {type(val).__name__} ...should be type {type(ano).__name__}"
        
            if len(ano) > 1:
                raise AssertionError(f"\'{par}\' annotation inconsistency: set should have 1 value but had {len(ano)} annotation = {ano}")
            
            for v in val:
                if not isinstance(v,list(ano)[0]):
                    raise AssertionError(f"\'{par}\' failed annotation check(wrong type): value = {v} was type {type(v).__name__} ...should be type {type(ano[0]).__name__}")
            
            
            
            
        def check_lambda(par, ano, val):
            if len(inspect.signature(ano).parameters) != 1:
                raise AssertionError(f"\'{par}\' annotation inconsistency: predicate should have 1 parameter but had {len(inspect.signature(ano).parameters)} predicate = {ano}")
            
            try:
                if type(val) is not list:
                    if not ano(val): 
                        raise AssertionError(f"\'{par}\' failed annotation check: value = {val} predicate = {ano} 1")
                else:
                    for v in val:
                        if not ano(v):
                            raise AssertionError(f"\'{par}\' failed annotation check: value = {v} predicate = {ano} list[{val.index(v)}] check: {ano}")
                            
                
            except:
                raise AssertionError(f"\'{par}\' failed annotation check: value = {val} predicate = {ano}")
    
        
        def check_else(par,ano,val):
            #print(par, type(par))
            #print(ano, type(ano))
            #print(val, type(val))
            
            if type(ano) == str and type(par) == dict:
                for k, v in par.items():
                    ano = ano.replace(k, str(v))
                try:
                    if not eval(ano):
                        raise AssertionError
                except NameError:
                    raise AssertionError
                
            elif type(ano) == str:
                try:
                    ano = ano.replace(par,str(val))
                    if not eval(ano):
                        raise AssertionError
                except NameError:
                    raise AssertionError
            else:
                try:
                    ano.__check_annotation__(self.check, par, val, check_history)
                except:
                    raise AssertionError(f"\'{par}\' annotation undecipherable: {ano.__repr__()}")
            
        #   lambda/functions, and str (str for extra credit)
        # Many of these local functions called by check, call check on their
        #   elements (thus are indirectly recursive)

        # We start by comparing check's function annotation to its arguments
        
        if annot == None:
            pass
        
        
        elif type(annot) is type:
            assert isinstance(value, annot), f"\'{param}\' failed annotation check(wrong type): value = {value} was type {type(value).__name__} ...should be type {annot.__name__}"
        
        
        elif annot is list:
            assert isinstance(value, list), f"\'{param}\' failed annotation check(wrong type): value = {value} was type {type(value).__name__} ...should be type {annot.__name__}"
        
        
        elif isinstance(annot,list):
            check_list(param, annot, value)
        

        elif isinstance(annot,tuple):
            check_tuple(param, annot, value)
        
        
        elif isinstance(annot, set):
            check_set(param, annot, value)
            
            
        elif isinstance(annot, frozenset):
            check_frozenset(param, annot, value)
        
        
        elif isinstance(annot, dict):
            check_dict(param, annot, value)
        
        
        elif inspect.isfunction(annot):
            check_lambda(param, annot, value)
            

        
        else:
            check_else(param, annot, value)
            
            
    def __call__(self, *args, **kargs):

        def param_arg_bindings():
            f_signature  = inspect.signature(self._f)
            bound_f_signature = f_signature.bind(*args,**kargs)
            for param in f_signature.parameters.values():
                if not (param.name in bound_f_signature.arguments):
                    bound_f_signature.arguments[param.name] = param.default
            return bound_f_signature.arguments
        
        
        if not self._checking_on:
            return param_arg_bindings()

        params = param_arg_bindings()
        annote = self._f.__annotations__
        
        
        try:
            # Check the annotation for each of the annotated parameters
            temp = []
            if type(list(annote.values())[0]) == str and len(list(params.keys())) > 1:
                self.check(params, list(annote.values())[0], params)
            else:
                for key, value in params.items():
                    self.check(key, annote[key], value)
                    temp.append(value)

            # Compute/remember the value of the decorated function
            if type(list(annote.values())[0]) == str and len(list(params.keys())) > 1:
                x = self._f(*tuple(params))
            else:
                x = self._f(temp[0])
            
            
            # If 'return' is in the annotation, check it
            if "return" in annote:
                if x is not None:
                    params["_return"] = x
            
            
            # Return the decorated answer
            #print(annote["return"], params["_return"], annote["return"] == type(params["_return"]))
            if "return" in annote:
                assert annote["return"] == type(params["_return"]), "\'return\' failed annotation check"
                
            return x
            
        # On first AssertionError, print the source lines of the function and reraise 
        except AssertionError:
            # print(80*'-')
            # print(inspect.getsource(self._f))
            # for l in inspect.getsourcelines(self._f)[0]: # ignore starting line #
            #     print(l.rstrip())
            # print(80*'-')
            raise 

  
if __name__ == '__main__':     
    # def f(x:int) -> str: pass
    # f = Check_Annotation(f)
    # f(3)
    # f('a')
           
    #driver tests
    import driver
    driver.default_file_name = 'bscp4S22.txt'
    driver.default_show_exception= True
    driver.default_show_exception_message= True
    driver.default_show_traceback= True
    driver.driver()
