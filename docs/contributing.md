# Contributing

ForgeStack should be easy to extend and safe to maintain.

## Contribution rules

1. Keep the core small.
2. Prefer plugins over core feature growth.
3. Avoid heavy dependencies in the core.
4. Preserve the planner/executor split.
5. Treat the graph as a first-class primitive.
6. Add docs for all new extension points.
7. Add tests for all new core behaviors.

## Architectural rule

Before adding something to the core, ask:

- Can this be a plugin?
- Can this be represented as a plan action?
- Does the core need to know about this system at all?

If the answer is no, keep it out of the core.
