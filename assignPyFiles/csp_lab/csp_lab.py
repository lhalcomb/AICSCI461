#from classify import *
import math

##
## CSP lab.
##
from csp import BinaryConstraint, CSP, CSPState, Variable,\
    basic_constraint_checker, solve_csp_problem

# Implement basic forward checking on the CSPState see csp.py
def forward_checking(state, verbose=False):
    # Before running Forward checking we must ensure
    # that constraints are okay for this state.
    basic = basic_constraint_checker(state, verbose)
    if not basic:
        return False

    x = state.get_current_variable()
    if x is None:
        return True
    
    x_value = x.get_assigned_value()
    for constraint in state.get_constraints_by_name(x.get_name()):
        y = state.get_variable_by_name(constraint.get_variable_j_name())
        if y.is_assigned():
            continue
        for y_value in y.get_domain():
            if not constraint.check(state, x_value, y_value):
                y.reduce_domain(y_value)
                if y.domain_size() == 0:
                    return False
    
    return True


    
    

# Now Implement forward checking + (constraint) propagation through
# singleton domains.
def forward_checking_prop_singleton(state, verbose=False):
    # Run forward checking first.
    fc_checker = forward_checking(state, verbose)
    if not fc_checker:
        return False

    # Add your propagate singleton logic here.
    raise NotImplementedError

## The code here are for the tester
## Do not change.
from moose_csp import moose_csp_problem
from map_coloring_csp import map_coloring_csp_problem

def csp_solver_tree(problem, checker):
    problem_func = globals()[problem]
    checker_func = globals()[checker]
    answer, search_tree = problem_func().solve(checker_func)
    return search_tree.tree_to_string(search_tree)



## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = ""
WHAT_I_FOUND_INTERESTING = ""
WHAT_I_FOUND_BORING = ""


## This function is used by the tester, please don't modify it!
def eval_test(eval_fn, group1, group2, verbose = 0):
    """ Find eval_fn in globals(), then execute evaluate() on it """
    # Only allow known-safe eval_fn's
    if eval_fn in [ 'my_classifier' ]:
        return evaluate(globals()[eval_fn], group1, group2, verbose)
    else:
        raise Exception("Error: Tester tried to use an invalid evaluation function: '%s'" % eval_fn)

    
