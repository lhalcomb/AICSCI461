import xmlrpc.client
import traceback
import sys
import os
import tarfile

try:
    from io import StringIO
except ImportError:
    from io import StringIO


# This is a skeleton for what the tester should do. Ideally, this module
# would be imported in the pset and run as its main function. 

# We need the following rpc functions. (They generally take username and
# password, but you could adjust this for whatever security system.)
#
# tester.submit_code(username, password, pset, studentcode)
#   'pset' is a string such as 'ps0'. studentcode is a string containing
#   the contents of the corresponding file, ps0.py. This stores the code on
#   the server so we can check it later for cheating, and is a prerequisite
#   to the tester returning a grade.
#
# tester.get_tests(pset)
#   returns a list of tuples of the form (INDEX, TYPE, NAME, ARGS):
#     INDEX is a unique integer that identifies the test.
#     TYPE should be one of either 'VALUE' or 'FUNCTION'.
#     If TYPE is 'VALUE', ARGS is ignored, and NAME is the name of a
#     variable to return for this test.  The variable must be an attribute
#     of the lab module.
#     If TYPE is 'FUNCTION', NAME is the name of a function in the lab module
#     whose return value should be the answer to this test, and ARGS is a
#     tuple containing arguments for the function.
#
# tester.send_answer(username, password, pset, index, answer)
#   Sends <answer> as the answer to test case <index> (0-numbered) in the pset
#   named <pset>. Returns whether the answer was correct, and an expected
#   value.
#
# tester.status(username, password, pset)
#   A string that includes the official score for this user on this pset.
#   If a part is missing (like the code), it should say so.

# Because I haven't written anything on the server side, test_online has never
# been tested.

def test_summary(dispindex, ntests, testname):
    return "Test %d/%d (%s)" % (dispindex, ntests, testname)

def show_result(testsummary, testcode, correct, got, expected, verbosity):
    """ Pretty-print test results """
    if correct:
        if verbosity > 0:
            print("%s: Correct." % testsummary)
        if verbosity > 1:
            print('\t', testcode)
            print()
    else:
        print("%s: Incorrect." % testsummary)
        print('\t', testcode)
        print("Got:     ", got)
        print("Expected:", expected)

def show_exception(testsummary, testcode):
    """ Pretty-print exceptions (including tracebacks) """
    print("%s: Error." % testsummary)
    print("While running the following test case:")
    print('\t', testcode)
    print("Your code encountered the following error:")
    traceback.print_exc()
    print()


def get_lab_module():
    # Try the easy way first
    try:
        from tests import lab_number
    except ImportError:
        lab_number = None
        
    if lab_number != None:
        lab = __import__('lab%s' % lab_number)
        return lab
        
    lab = None

    for labnum in range(10):
        try:
            lab = __import__('lab%s' % labnum)
        except ImportError:
            pass

    if lab == None:
        raise ImportError("Cannot find your lab; or, error importing it.  Try loading it by running 'python labN.py' (for the appropriate value of 'N').")

    if not hasattr(lab, "LAB_NUMBER"):
        lab.LAB_NUMBER = labnum
    
    return lab

def type_decode(arg, lab):
    """
    XMLRPC can only pass a very limited collection of types.
    Frequently, we want to pass a subclass of 'list' in as a test argument.
    We do that by converting the sub-type into a regular list of the form:
    [ 'TYPE', (data) ] (ie., AND(['x','y','z']) becomes ['AND','x','y','z']).
    This function assumes that TYPE is a valid attr of 'lab' and that TYPE's
    constructor takes a list as an argument; it uses that to reconstruct the
    original data type.
    """
    if isinstance(arg, list) and len(arg) >= 1: # We'll leave tuples reserved for some other future magic
        try:
            mytype = arg[0]
            data = arg[1:]
            return getattr(lab, mytype)([ type_decode(x, lab) for x in data ])
        except AttributeError:
            return [ type_decode(x, lab) for x in arg ]
        except TypeError:
            return [ type_decode(x, lab) for x in arg ]
    else:
        return arg

    
def type_encode(arg):
    """
    Encode trees as lists in a way that can be decoded by 'type_decode'
    """
    if isinstance(arg, list) and not type(arg) in (list,tuple):
        return [ arg.__class__.__name__ ] + [ type_encode(x) for x in arg ]
    elif hasattr(arg, '__class__') and arg.__class__.__name__ == 'IF':
        return [ 'IF', type_encode(arg._conditional), type_encode(arg._action), type_encode(arg._delete_clause) ]
    else:
        return arg

    
def run_test(test, lab):
    """
    Takes a 'test' tuple as provided by the online tester
    (or generated by the offline tester) and executes that test,
    returning whatever output is expected (the variable that's being
    queried, the output of the function being called, etc)

    'lab' (the argument) is the module containing the lab code.
    
    'test' tuples are in the following format:
      'id': A unique integer identifying the test
      'type': One of 'VALUE', 'FUNCTION', 'MULTIFUNCTION', or 'FUNCTION_ENCODED_ARGS'
      'attr_name': The name of the attribute in the 'lab' module
      'args': a list of the arguments to be passed to the function; [] if no args.
      For 'MULTIFUNCTION's, a list of lists of arguments to be passed in
    """
    id, mytype, attr_name, args = test

    attr = getattr(lab, attr_name)

    if mytype == 'VALUE':
        return attr
    elif mytype == 'FUNCTION':
        return attr(*args)
    elif mytype == 'MULTIFUNCTION':
        return [ run_test( (id, 'FUNCTION', attr_name, FN), lab) for FN in args ]
    elif mytype == 'FUNCTION_ENCODED_ARGS':
        return run_test( (id, 'FUNCTION', attr_name, type_decode(args, lab)), lab )
    else:
        raise Exception("Test Error: Unknown TYPE '%s'.  Please make sure you have downloaded the latest version of the tester script.  If you continue to see this error, contact a TA.")


def test_offline(verbosity=1):
    """ Run the unit tests in 'tests.py' """
    import tests as tests_module
    
#    tests = [ (x[:-8],
#               getattr(tests_module, x),
#               getattr(tests_module, "%s_testanswer" % x[:-8]),
#               getattr(tests_module, "%s_expected" % x[:-8]),
#               "_".join(x[:-8].split('_')[:-1]))
#              for x in tests_module.__dict__.keys() if x[-8:] == "_getargs" ]

    tests = tests_module.get_tests()
    
    ntests = len(tests)
    ncorrect = 0
    
    for index, (testname, getargs, testanswer, expected, fn_name, type) in enumerate(tests):
        dispindex = index+1
        summary = test_summary(dispindex, ntests, fn_name)
        
        try:
            if callable(getargs):
                getargs = getargs()
                
#            answer = run_test((index, type, fn_name, getargs), get_lab_module())
            lab = __import__ ('csp_lab')
            answer = run_test((index, type, fn_name, getargs), lab)
        except NotImplementedError:
            print("%d: (%s: Function not yet implemented, NotImplementedError raised)" % (index, testname))
            continue
        except Exception:
            show_exception(summary, testname)
            continue
        
        correct = testanswer(answer, original_val = getargs)
        show_result(summary, testname, correct, answer, expected, verbosity)
        if correct: ncorrect += 1
    
    print("Passed %d of %d tests." % (ncorrect, ntests))
    return ncorrect == ntests

def get_target_upload_filedir():
    """ Get, via user prompting, the directory containing the current lab """
    cwd = os.getcwd() # Get current directory.  Play nice with Unicode pathnames, just in case.
        
    print("Please specify the directory containing your lab.")
    print("Note that all files from this directory will be uploaded!")
    print("Labs should not contain large amounts of data; very-large")
    print("files will fail to upload.")
    print()
    print("The default path is '%s'" % cwd)
    target_dir = input("[%s] >>> " % cwd)

    target_dir = target_dir.strip()
    if target_dir == '':
        target_dir = cwd

    print("Ok, using '%s'." % target_dir)

    return target_dir

def get_tarball_data(target_dir, filename):
    """ Return a binary String containing the binary data for a tarball of the specified directory """
    data = StringIO()
    file = tarfile.open(filename, "w|bz2", data)

    print("Preparing the lab directory for transmission...")
            
    file.add(target_dir+"/lab4.py")
    
    print("Done.")
    print()
    print("The following files have been added:")
    
    for f in file.getmembers():
        print(f.name)
            
    file.close()

    return data.getvalue()
    

def test_online(verbosity=1):
    """ Run online unit tests.  Run them against the 6.034 server via XMLRPC. """
    lab = get_lab_module()

    try:
        server = xmlrpc.client.Server(server_url, allow_none=True)
        #print "Getting tests:", (username, password, lab.__name__)
        tests = server.get_tests(username, password, lab.__name__)
        #print "*** TESTS:"
        #print tests

    except NotImplementedError: # Solaris Athena doesn't seem to support HTTPS
        print("Your version of Python doesn't seem to support HTTPS, for")
        print("secure test submission.  Would you like to downgrade to HTTP?")
        print("(note that this could theoretically allow a hacker with access")
        print("to your local network to find your 6.034 password)")
        answer = input("(Y/n) >>> ")
        if len(answer) == 0 or answer[0] in "Yy":
            server = xmlrpc.client.Server(server_url.replace("https", "http"))
            tests = server.get_tests(username, password, lab.__name__)
        else:
            print("Ok, not running your tests.")
            print("Please try again on another computer.")
            print("Linux Athena computers are known to support HTTPS,")
            print("if you use the version of Python in the 'python' locker.")
            sys.exit(0)
            
    ntests = len(tests)
    ncorrect = 0

    lab = get_lab_module()
    
    target_dir = get_target_upload_filedir()

    tarball_data = get_tarball_data(target_dir, "lab%s.tar.bz2" % lab.LAB_NUMBER)
            
    print("Submitting to the 6.034 Webserver...")

    server.submit_code(username, password, lab.__name__, xmlrpc.client.Binary(tarball_data))

    print("Done submitting code.")
    print("Running test cases...")
    
    for index, testcode in enumerate(tests):
        dispindex = index+1
        summary = test_summary(dispindex, ntests, testcode)

        try:
            answer = run_test(testcode, get_lab_module())
        except Exception:
            show_exception(summary, testcode)
            continue

        correct, expected = server.send_answer(username, password, lab.__name__, testcode[0], type_encode(answer))
        show_result(summary, testcode, correct, answer, expected, verbosity)
        if correct: ncorrect += 1
    
    response = server.status(username, password, lab.__name__)
    print(response)



if __name__ == '__main__':
    test_offline()
    
def make_test_counter_decorator():
    tests = []
    def make_test(getargs, testanswer, expected_val, name = None, type = 'FUNCTION'):
        if name != None:
            getargs_name = name
        elif not callable(getargs):
            getargs_name = "_".join(getargs[:-8].split('_')[:-1])
            getargs = lambda: getargs
        else:
            getargs_name = "_".join(getargs.__name__[:-8].split('_')[:-1])
            
        tests.append( ( getargs_name,
                        getargs,
                        testanswer,
                        expected_val,
                        getargs_name,
                        type ) )

    def get_tests():
        return tests

    return make_test, get_tests


make_test, get_tests = make_test_counter_decorator()
