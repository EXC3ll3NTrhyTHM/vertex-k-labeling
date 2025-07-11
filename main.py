from src.graph_generator import create_mongolian_tent_graph
from src.graph_properties import calculate_lower_bound, calculate_graph_metrics, is_regular, compute_diameter
from src.labeling_solver import find_feasible_k_labeling, find_optimal_k_labeling
import json
import time
import argparse
from src.edge_irregular_solver import k_labeling_backtracking
from src.constants import DEFAULT_TENT_SIZE, DEFAULT_SOLVER_TYPE, DEFAULT_CIRCULANT_OFFSET
from src.graph_generator import generate_circulant_graph

def main():
    """
    Main function to find a feasible k-labeling for a Mongolian Tent graph.
    """
    parser = argparse.ArgumentParser(description="Find and visualize k-labeling for Mongolian Tent graphs.")
    parser.add_argument("--n", type=int, default=DEFAULT_TENT_SIZE, help=f"Value of n (default: {DEFAULT_TENT_SIZE})")
    parser.add_argument("--graph-type", type=str, default="shape", choices=["shape", "circulant"], help="Graph type: 'shape' (Mongolian Tent) or 'circulant' (r = max(n - DEFAULT_CIRCULANT_OFFSET, 2))")
    parser.add_argument("--solver", type=str, default=DEFAULT_SOLVER_TYPE, choices=["heuristic", "backtracking", "edge-irregular", "branch-and-bound"], help=f"Solver to use: 'heuristic', 'backtracking', 'edge-irregular', or 'branch-and-bound' (default: {DEFAULT_SOLVER_TYPE})")
    parser.add_argument("--k-limit", type=int, default=None, help="Upper bound on k for edge-irregular solver")
    parser.add_argument("--progress", action="store_true", help="Print progress of k-limit search for edge-irregular solver")
    parser.add_argument("--heuristic_mode", type=str, default="accurate", choices=["accurate", "fast", "intelligent"], help="Heuristic mode: 'accurate' uses randomized multi-attempt search (slower, better chance of optimal k), 'fast' uses a single-pass greedy (faster, possibly higher k), 'intelligent' uses a degree-biased and conflict-minimizing approach. Ignored for backtracking solver.")
    parser.add_argument(
        "--animate",
        type=str,
        default="off",
        choices=["off", "live", "record"],
        help="Enable animated visualization (live window or record to GIF/MP4).",
    )
    args = parser.parse_args()

    n = args.n
    solver_type = args.solver
    heuristic_mode = args.heuristic_mode

    print(f"Finding a {solver_type} k-labeling for {args.graph_type} graph with n = {n}")
    # Generate the selected graph type
    if args.graph_type == "circulant":
        # Degree r defaults to n - DEFAULT_CIRCULANT_OFFSET, minimum 2
        r = max(n - DEFAULT_CIRCULANT_OFFSET, 2)
        graph = generate_circulant_graph(n, r)
    else:
        # 'shape' refers to Mongolian Tent graph
        graph = create_mongolian_tent_graph(n)
    
    if args.graph_type == "circulant":
        # Degree r defaults to n - DEFAULT_CIRCULANT_OFFSET, minimum 2
        r = max(n - DEFAULT_CIRCULANT_OFFSET, 2)
        # Compute properties
        edges, max_deg = calculate_graph_metrics(graph)
        diam = compute_diameter(graph)
        print(f"Circulant graph C_{{{n},{r}}}: vertices={len(graph)}, edges={edges}, degree={max_deg}, diameter={diam}")
        # Visualize circulant graph without k-labeling
        try:
            from src.visualization import visualize_k_labeling
            file_name = f"graphs/circulant_{n}_{r}.png"
            visualize_k_labeling(graph, {}, output=file_name, shaped=False)
            print(f"Visualization saved to {file_name}")
        except ImportError:
            print("Graphviz not installed; skipping visualization.")
        return
    # Proceed with solver for shape graphs
    # Setup callbacks based on animation mode
    anim_ctrl = None
    events = None
    on_step_cb = None
    on_event_cb = None
    if args.animate == "live":
        from src.visualization.animation import AnimationController

        anim_ctrl = AnimationController(graph, mode="live")
        on_step_cb = anim_ctrl.update
    elif args.animate == "record":
        from src.visualization.recorder import EventRecorder

        events = []
        recorder = EventRecorder(events)
        on_event_cb = recorder
    else:
        on_step_cb = None
        on_event_cb = None

    start_time = time.time()
    if solver_type == "heuristic":
        k, labeling = find_feasible_k_labeling(
            n,
            algorithm=heuristic_mode,
            on_step=on_step_cb,
            on_event=on_event_cb,
        )
        lower_bound = calculate_lower_bound(n)
        gap = (k - lower_bound) if isinstance(k, int) else "N/A"
        solver_name = "Heuristic"
    elif solver_type == "backtracking":
        k, labeling = find_optimal_k_labeling(
            n,
            on_step=on_step_cb,
            on_event=on_event_cb,
        )
        lower_bound = k  # Optimal solver finds minimal k
        gap = 0
        solver_name = "Backtracking"
    elif solver_type == "edge-irregular":
        # Edge-Irregular backtracking solver
        labeling = k_labeling_backtracking(graph, k_limit=args.k_limit)
        if labeling:
            k = max(labeling.values())
        else:
            k = None
        lower_bound = max((len(neighbors) for neighbors in graph.values()), default=0)
        gap = k - lower_bound if isinstance(k, int) else "N/A"
        solver_name = "Edge-Irregular Backtracking"
    elif solver_type == "branch-and-bound":
        from src.labeling_solver import BranchAndBoundSolver
        solver = BranchAndBoundSolver(n, on_step=on_step_cb)
        k, labeling = solver.find_es()
        lower_bound = k # Branch and Bound finds the optimal k
        gap = 0
        solver_name = "Branch and Bound"
    else:
        print("Invalid solver type. Please choose 'heuristic', 'backtracking', 'edge-irregular', or 'branch-and-bound'.")
        return
    end_time = time.time()
    time_taken = end_time - start_time

    if labeling:
        print(f"\n{solver_name} k found: {k}")
        print(f"Theoretical lower bound for k: {lower_bound}")
        print(f"Gap to lower bound: {gap}")
        print(f"Time taken to find k: {time_taken:.2f} seconds")

        # --- Visualization Example ---
        try:
            from src.visualization import visualize_k_labeling

            # Determine filename and display name depending on solver type
            if solver_type == "heuristic":
                file_name = f"graphs/mt3_{n}_{solver_type}_{heuristic_mode}.png"
                display_solver_name = f"{solver_name} ({heuristic_mode})"
            else:
                file_name = f"graphs/mt3_{n}_{solver_type}.png"
                display_solver_name = solver_name

            visualize_k_labeling(
                graph,
                labeling,
                output=file_name,
                shaped=(args.graph_type == "shape"),
                heuristic_k=k,
                lower_bound_k=lower_bound,
                gap=gap,
                time_taken=time_taken,
                solver_name=display_solver_name,
            )
            print(f"Visualization saved to {file_name}")
        except ImportError:
            print("Graphviz not installed; skipping visualization.")

        # Save animation if recorded (post-solve replay)
        if args.animate == "record":
            from src.visualization.replay import ReplayController

            # Use empty list if events is unexpectedly None
            replayer = ReplayController(graph, events or [])
            outfile = f"graphs/solver_run_n{n}_{solver_type}.gif"
            try:
                path = replayer.save(outfile)
                print(f"Recording saved to {path}")
            except Exception as err:
                print(f"Failed to save recording: {err}")
    else:
        print(f"Could not find a valid labeling for n = {n}")

if __name__ == "__main__":
    main()
