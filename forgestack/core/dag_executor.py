from concurrent.futures import ThreadPoolExecutor, as_completed


def execute_dag(graph, registry, ctx_factory, max_workers=4):
    """
    Execute plugins in dependency-safe waves.

    graph.edges[A] = {B, C} means A depends on B and C
    """

    completed = set()
    remaining = set(graph.resolved)
    execution_order = []

    while remaining:

        ready = []

        for node in remaining:
            deps = graph.edges.get(node, set())
            if deps.issubset(completed):
                ready.append(node)

        ready = sorted(ready)
        print("EXECUTION WAVE:", ready)

        if not ready:
            raise RuntimeError(
                "No executable nodes found. Graph may contain a cycle."
            )

        wave_results = []

        with ThreadPoolExecutor(max_workers=max_workers) as pool:

            futures = {}

            for name in ready:
                plugin = registry.get(name)
                ctx = ctx_factory(name)
                futures[pool.submit(plugin.plan, ctx)] = name

            for future in as_completed(futures):
                name = futures[future]
                future.result()
                wave_results.append(name)

        for name in sorted(wave_results):
            completed.add(name)
            remaining.remove(name)
            execution_order.append(name)

    return execution_order