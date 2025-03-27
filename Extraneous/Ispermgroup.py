from sympy.combinatorics import Permutation, PermutationGroup

# Define permutations in cycle notation
A = [
    Permutation(1, 2, 3, 4, 5),  # Corrected: Elements as individual arguments
    Permutation(1, 4, 5, 3, 2),
    Permutation(2, 3, 5, 4),
    Permutation(1, 2),
    Permutation([])  # Identity permutation
]

# Generate the permutation group from A
G = PermutationGroup(A)

# Check closure: Compute all products and verify they stay in A
closure_check = all((p1 * p2) in G for p1 in A for p2 in A)

# Check inverses: Ensure each permutation has an inverse in A
inverse_check = all(p**-1 in G for p in A)

# Print results
print("Closure under composition:", closure_check)
print("Every element has an inverse:", inverse_check)

# Final check: If both hold, it's a group
if closure_check and inverse_check:
    print("A forms a permutation group!")
else:
    print("A is NOT a permutation group.")