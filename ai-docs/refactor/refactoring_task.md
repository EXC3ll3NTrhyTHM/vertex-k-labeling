# Project Refactoring Task

This document outlines a comprehensive refactoring plan for the vertex-k-labeling project to improve code readability, maintainability, and performance.

## Overview

The refactoring will focus on four main areas:
1. **Naming Conventions** - Improve function, parameter, and variable names for better readability
2. **Code Cleanup** - Remove commented-out code and dead code
3. **Algorithm Optimization** - Review and optimize core algorithms
4. **Unit Test Updates** - Ensure tests match refactored code and provide adequate coverage

## Task 1: Naming Convention Improvements

### 1.1 Function Renaming

**Current Issues:**
- `_is_valid_assignment` - underscore prefix suggests private but used across modules
- `find_minimum_k_labeling` - verbose and inconsistent with `find_heuristic_labeling`
- `greedy_labeling_solver` - "solver" suffix inconsistent
- `backtracking_solver` - should be private or renamed
- `get_graph_properties` - generic name doesn't indicate what properties

**Proposed Changes:**
```python
# Current → Proposed
_is_valid_assignment → is_labeling_valid
find_minimum_k_labeling → find_optimal_k_labeling
find_heuristic_labeling → find_feasible_k_labeling
greedy_labeling_solver → greedy_k_labeling
backtracking_solver → _backtrack_k_labeling (make private)
get_graph_properties → calculate_graph_metrics
generate_mongolian_tent_graph → create_mongolian_tent_graph
```

### 1.2 Parameter and Variable Renaming

**Current Issues:**
- Single letter variables (`k`, `n`, `v`, `u`) lack context
- Generic names (`graph`, `labeling`) could be more specific
- Inconsistent naming patterns

**Proposed Changes:**
```python
# Parameters
k → k_value or max_k_value (context dependent)
n → tent_size or graph_size
graph → adjacency_list or vertex_graph
labeling → vertex_labels or k_labeling
vertices_to_label → unlabeled_vertices

# Variables
u, v → source_vertex, target_vertex (in edge contexts)
lbl → label_value
nbrs → neighbors
max_k → k_upper_bound
```

### 1.3 Constant and Configuration Naming

```python
# Add meaningful constants
DEFAULT_TENT_SIZE = 5
DEFAULT_SOLVER_TYPE = "heuristic"
MAX_K_MULTIPLIER_DEFAULT = 20
GREEDY_ATTEMPTS_DEFAULT = 100
```

## Task 2: Code Cleanup

### 2.1 Remove Commented Code

**Files to clean:**
- `src/labeling_solver.py` - Remove commented greedy optimization section (lines ~87-100)
- Review all files for TODO comments and outdated comments
- Remove any debug print statements that are no longer needed

### 2.2 Dead Code Removal

**Areas to review:**
- Unused imports
- Unreachable code paths
- Redundant validation checks
- Obsolete helper functions

### 2.3 Documentation Cleanup

- Update docstrings to match new function names
- Ensure all public functions have comprehensive docstrings
- Remove outdated inline comments
- Add type hints where missing

## Task 3: Algorithm Optimization

### 3.1 Core Algorithm Review

**`is_labeling_valid` function:**
- Review string comparison logic for vertex ordering
- Consider using vertex IDs instead of string conversion
- Optimize edge weight collection to avoid redundant iterations

**`greedy_k_labeling` function:**
- Review randomization strategy effectiveness
- Consider deterministic fallback when randomization fails
- Optimize label selection order

**`_backtrack_k_labeling` function:**
- Review vertex ordering heuristic (degree-based sorting)
- Consider additional pruning strategies
- Optimize partial validation calls

### 3.2 Performance Optimizations

**Memory usage:**
- Use generators where appropriate
- Optimize data structures (consider using sets for faster lookups)
- Reduce temporary object creation

**Computational efficiency:**
- Cache frequently computed values
- Avoid redundant graph property calculations
- Optimize nested loops in validation

### 3.3 Algorithm Logic Review

**Validation logic:**
- Ensure `last_vertex` optimization in `is_labeling_valid` is correct
- Verify edge weight uniqueness checking
- Review partial vs. complete validation scenarios

**Search strategy:**
- Evaluate vertex ordering heuristics
- Consider alternative search strategies for backtracking
- Review termination conditions

## Task 4: Unit Test Updates

### 4.1 Test Function Renaming

Update all test functions to match refactored code:
```python
# Example updates needed
test_is_valid_assignment → test_is_labeling_valid
test_find_minimum_k_labeling → test_find_optimal_k_labeling
test_greedy_labeling_solver → test_greedy_k_labeling
```

### 4.2 Test Coverage Review

**Current test files to update:**
- `tests/test_labeling_solver.py`
- `tests/test_graph_properties.py`
- `tests/test_graph_generator.py`
- `tests/test_visualization.py`

**Coverage improvements needed:**
- Edge cases for small graphs (n=1, n=2)
- Invalid input handling
- Performance benchmarks for different algorithm variants
- Validation of optimization correctness

### 4.3 Test Data and Fixtures

- Create standard test graphs as fixtures
- Add parametrized tests for different graph sizes
- Include regression tests for known optimal k values

## Task 5: Implementation Plan

### Phase 1: Naming Refactor (Priority: High)
1. Update function names in `src/` modules
2. Update parameter names and docstrings
3. Update imports across all files
4. Update `main.py` to use new function names

### Phase 2: Code Cleanup (Priority: High)
1. Remove commented code from `src/labeling_solver.py`
2. Clean up imports and unused code
3. Update documentation and docstrings

### Phase 3: Algorithm Optimization (Priority: Medium)
1. Optimize `is_labeling_valid` function
2. Review and improve vertex ordering strategies
3. Implement performance enhancements

### Phase 4: Test Updates (Priority: High)
1. Update test function names and imports
2. Fix any broken tests due to refactoring
3. Add missing test coverage
4. Verify all tests pass

### Phase 5: Documentation Update (Priority: Low)
1. Update README.md with new function names
2. Update AI documentation in `ai-docs/`
3. Add code examples with new naming

## Acceptance Criteria

- [ ] All functions follow consistent naming conventions
- [ ] No commented-out code remains
- [ ] All algorithms maintain correctness while improving performance
- [ ] Test suite achieves >90% code coverage
- [ ] All existing functionality preserved
- [ ] Performance benchmarks show no regression
- [ ] Documentation reflects all changes

## Risk Assessment

**Low Risk:**
- Function and variable renaming
- Documentation updates
- Test name updates

**Medium Risk:**
- Algorithm optimization changes
- Removing commented code (ensure no needed functionality)

**High Risk:**
- Core validation logic changes
- Major algorithm restructuring

## Timeline Estimate

- **Phase 1-2 (Naming + Cleanup):** 1-2 days
- **Phase 3 (Algorithm Optimization):** 2-3 days
- **Phase 4 (Test Updates):** 1-2 days
- **Phase 5 (Documentation):** 1 day

**Total Estimated Time:** 5-8 days

## Notes

- Maintain backward compatibility where possible
- Create feature branch for refactoring work
- Consider performance benchmarks before and after optimization
- Ensure all team members review naming convention changes 