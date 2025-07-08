# Task 1: Naming Convention Improvements

## Goal
Improve code readability and maintainability by implementing consistent naming conventions across all functions, parameters, variables, and constants in the vertex-k-labeling project.

## High Level Overview
This task focuses on renaming functions, parameters, and variables to follow Python naming conventions and improve code clarity. The refactoring will make the codebase more intuitive for developers and maintain consistency across all modules.

**Key Areas:**
1. Function renaming for clarity and consistency
2. Parameter and variable renaming for better context
3. Introduction of meaningful constants
4. Update all imports and references
- Add adherence to PEP 8 naming conventions

## Detailed Steps

### 1.1 Function Renaming in Core Modules

#### 1.1.1 Update `src/labeling_solver.py`
- [x] Rename `_is_valid_assignment` to `is_labeling_valid`
  - [x] Update function definition
  - [x] Update all internal calls within the file
  - [x] Update docstring
- [x] Rename `find_minimum_k_labeling` to `find_optimal_k_labeling`
  - [x] Update function definition
  - [x] Update all internal calls within the file
  - [x] Update docstring
- [x] Rename `greedy_labeling_solver` to `greedy_k_labeling`
  - [x] Update function definition
  - [x] Update all internal calls within the file
  - [x] Update docstring
- [x] Rename `backtracking_solver` to `_backtrack_k_labeling` (make private)
  - [x] Update function definition
  - [x] Update all internal calls within the file
  - [x] Update docstring
- [x] Rename `find_heuristic_labeling` to `find_feasible_k_labeling`
  - [x] Update function definition
  - [x] Update docstring

#### 1.1.2 Update `src/graph_properties.py`
- [x] Rename `get_graph_properties` to `calculate_graph_metrics`
  - [x] Update function definition
  - [x] Update all internal calls within the file
  - [x] Update docstring

#### 1.1.3 Update `src/graph_generator.py`
- [x] Rename `generate_mongolian_tent_graph` to `create_mongolian_tent_graph`
  - [x] Update function definition
  - [x] Update docstring

#### 1.1.4 Update `src/visualization.py`
- [x] Rename helper `_vertex_id` to `format_vertex_id`
  - [x] Update function definition
  - [x] Update all calls to `format_vertex_id` within the file
- [x] Rename `visualize_labeling` to `visualize_k_labeling`
  - [x] Update function definition and export in `__all__`
  - [x] Update calls in `main.py` and any other references

### 1.2 Parameter and Variable Renaming

#### 1.2.1 Update `src/labeling_solver.py` Parameters
- [x] In `is_labeling_valid`:
  - [x] Rename `graph` to `adjacency_list`
  - [x] Rename `labeling` to `vertex_labels`
  - [x] Update all references within function
- [x] In `find_optimal_k_labeling`:
  - [x] Rename `n` to `tent_size`
  - [x] Update all references within function
- [x] In `_backtrack_k_labeling`:
  - [x] Rename `graph` to `adjacency_list`
  - [x] Rename `labeling` to `vertex_labels`
  - [x] Rename `vertices_to_label` to `unlabeled_vertices`
  - [x] Rename `k` to `max_k_value`
  - [x] Update all references within function
- [x] In `greedy_k_labeling`:
  - [x] Rename `graph` to `adjacency_list`
  - [x] Rename `max_k` to `k_upper_bound`
  - [x] Update all references within function
- [x] In `find_feasible_k_labeling`:
  - [x] Rename `n` to `tent_size`
  - [x] Update all references within function

#### 1.2.2 Update `src/graph_properties.py` Parameters
- [ ] In `calculate_graph_metrics`:
  - [ ] Rename `graph` to `adjacency_list`
  - [ ] Update all references within function
- [ ] In `calculate_lower_bound`:
  - [ ] Rename `n` to `tent_size`
  - [ ] Update all references within function

#### 1.2.3 Update `src/graph_generator.py` Parameters
- [ ] In `create_mongolian_tent_graph`:
  - [ ] Rename `n` to `tent_size`
  - [ ] Update all references within function

#### 1.2.4 Update Local Variables
- [ ] In `is_labeling_valid`:
  - [ ] Rename `u, v` to `source_vertex, target_vertex` in edge contexts
  - [ ] Update all references
- [ ] In `find_feasible_k_labeling`:
  - [ ] Rename `max_k` to `k_upper_bound`
  - [ ] Update all references
- [ ] In `greedy_k_labeling`:
  - [ ] Rename `lbl` to `label_value` (if present)
  - [ ] Update all references
- [ ] Rename `nbrs` (in edge loops) to `neighbors`

### 1.3 Add Meaningful Constants

#### 1.3.1 Create constants file `src/constants.py`
- [x] Create new file `src/constants.py`
- [x] Add the following constants:
  ```python
  DEFAULT_TENT_SIZE = 5
  DEFAULT_SOLVER_TYPE = "heuristic"
  MAX_K_MULTIPLIER_DEFAULT = 20
  GREEDY_ATTEMPTS_DEFAULT = 100
  ```

#### 1.3.2 Update `main.py` to use constants
- [x] Import constants from `src.constants`
- [x] Replace hardcoded values with constants:
  - [x] Replace `5` with `DEFAULT_TENT_SIZE`
  - [x] Replace `"heuristic"` with `DEFAULT_SOLVER_TYPE`

#### 1.3.3 Update `src/labeling_solver.py` to use constants
- [ ] Import constants from `src.constants`
- [ ] Replace hardcoded values:
  - [ ] Replace `20` with `MAX_K_MULTIPLIER_DEFAULT`
  - [ ] Replace `100` with `GREEDY_ATTEMPTS_DEFAULT`

### 1.4 Update All Import Statements

#### 1.4.1 Update `main.py`
- [x] Update import: `from src.labeling_solver import find_feasible_k_labeling` and `find_optimal_k_labeling`
- [x] Update function calls to use `find_feasible_k_labeling` (heuristic), `find_optimal_k_labeling` (backtracking)
- [x] Update import and calls for visualization: `from src.visualization import visualize_k_labeling` and replace calls to `visualize_labeling`
- [x] Add import: `from src.constants import DEFAULT_TENT_SIZE, DEFAULT_SOLVER_TYPE`

#### 1.4.2 Update `src/labeling_solver.py`
- [x] Update import: `from src.graph_generator import create_mongolian_tent_graph`
- [ ] Add import: `from src.constants import MAX_K_MULTIPLIER_DEFAULT, GREEDY_ATTEMPTS_DEFAULT`

#### 1.4.3 Update `src/graph_properties.py`
- [x] Update import: `from src.graph_generator import create_mongolian_tent_graph`

#### 1.4.4 Update `src/visualization.py`
- [x] Update import: `from src.labeling_solver import is_labeling_valid`
- [x] Update function export in `__all__` to `visualize_k_labeling`
- [x] Update calls inside `visualize_k_labeling`: replace `_is_valid_assignment` with `is_labeling_valid` and rename any references accordingly
- [x] Rename helper calls: update all `format_vertex_id` references

### 1.5 Update Docstrings and Type Hints

#### 1.5.1 Update `src/labeling_solver.py` docstrings
- [ ] Update `is_labeling_valid` docstring with new parameter names
- [ ] Update `find_optimal_k_labeling` docstring
- [ ] Update `_backtrack_k_labeling` docstring
- [ ] Update `greedy_k_labeling` docstring
- [ ] Update `find_feasible_k_labeling` docstring

#### 1.5.2 Update `src/graph_properties.py` docstrings
- [ ] Update `calculate_graph_metrics` docstring
- [ ] Update `calculate_lower_bound` docstring

#### 1.5.3 Update `src/graph_generator.py` docstrings
- [ ] Update `create_mongolian_tent_graph` docstring

#### 1.5.4 Add missing type hints
- [ ] Add type hints to all updated functions
- [ ] Ensure consistency across all modules

### 1.6 Verification and Testing

#### 1.6.1 Syntax and Import Verification
- [ ] Run `python -m py_compile` on all modified files
- [ ] Run style linter (e.g., `flake8`) to ensure PEP 8 compliance
- [ ] Verify no syntax errors
- [ ] Test all imports work correctly

#### 1.6.2 Functionality Testing
- [ ] Run `python main.py` to ensure basic functionality works
- [ ] Test both heuristic and backtracking solvers
- [ ] Verify visualization still works

#### 1.6.3 Unit Test Compatibility Check
- [ ] Run existing unit tests to identify what breaks
- [ ] Create list of tests that need updating (for Task 4)
- [ ] Ensure no critical functionality is lost

## Acceptance Criteria

- [ ] All function names follow consistent naming conventions
- [ ] All parameter names provide clear context
- [ ] All variable names are descriptive and consistent
- [ ] Constants are defined and used appropriately
- [ ] All imports are updated and working
- [ ] All docstrings reflect new naming
- [ ] No syntax errors in any file
- [ ] Basic functionality is preserved
- [ ] Code is more readable and maintainable
- [ ] No references remain to old helper or visualization function names
- [ ] All function, parameter, and variable names conform to PEP 8 snake_case conventions
- [ ] All constants are UPPER_CASE and defined appropriately
- [ ] No commented-out or dead code remains
- [ ] Code passes linting (PEP 8) and syntax checks

## Notes

- **Backup**: Create a backup branch before starting
- **Testing**: Test after each major section to catch issues early
- **Linting**: Run `flake8` or similar after renaming to catch style issues
- **Documentation**: Keep track of changes for updating tests later
- **Consistency**: Ensure naming patterns are consistent across all modules
- **IDE Support**: Use IDE refactoring tools where possible to reduce manual errors
- **Commit Guidelines**: Commit after each completed subtask with descriptive messages

## Estimated Time
**2-3 hours** for careful, methodical completion of all steps with testing. 