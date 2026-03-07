# Planner

The planner converts plugin declarations into a concrete execution plan.

Steps:

1. Resolve plugin dependencies
2. Build dependency graph
3. Sort plugins
4. Execute planning hooks
5. Collect actions
6. Validate plan