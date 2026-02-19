# php_async_entry.py
from args_parser import build_parser
from launch_task import launch_task_mp
import file_tools
import threading
import sys
from nanoparticles_pack.snowflake import Triangle, Square, Pentagon, Hexagon
from nanoparticles_pack.others import ThreeWayJunction

def async_task(args, timestamp):
    shape_map = {
        "triangle": Triangle,
        "square": Square,
        "pentagon": Pentagon,
        "hexagon": Hexagon,
        "3wj": ThreeWayJunction
    }
    shape_class = shape_map[args.shape]

    constraints = {
        "minimumFreeEnergy": {},
        "mfeFrequency": {},
        "mfeDiversity": {}
    }
    if args.min_mfe is not None:
        constraints["minimumFreeEnergy"]["min"] = args.min_mfe
    if args.max_mfe is not None:
        constraints["minimumFreeEnergy"]["max"] = args.max_mfe
    if args.min_mfe_frequency is not None:
        constraints["mfeFrequency"]["min"] = args.min_mfe_frequency
    if args.max_mfe_frequency is not None:
        constraints["mfeFrequency"]["max"] = args.max_mfe_frequency
    if args.min_mfe_diversity is not None:
        constraints["mfeDiversity"]["min"] = args.min_mfe_diversity
    if args.max_mfe_diversity is not None:
        constraints["mfeDiversity"]["max"] = args.max_mfe_diversity

    gc_clasp_length = getattr(args, "gc_clasp_length", None)
    overhang_length = getattr(args, "overhang_length", None)

    launch_task_mp(
        sirna_path=args.sirna_path,
        shape=shape_class,
        quantity=args.quantity,
        max_quantity=args.max_quantity,
        substitute_ratio=args.substitute_ratio,
        n_processes=args.processes,
        output_format=args.output_format,
        output_filename=args.output_filename,
        constraints=constraints,
        gc_clasp_length=gc_clasp_length,
        overhang_length=overhang_length,
        timestamp=timestamp
    )




def main():
    parser = build_parser()
    args = parser.parse_args()

    timestamp = file_tools.generate_timestamp()
    res_path = file_tools.build_result_path(
        base_path="./tasks",
        timestamp=timestamp,
        filename=args.output_filename,
        suffix=args.output_format
    )

    print(res_path)
    sys.stdout.flush()

    thread = threading.Thread(target=async_task, args=(args, timestamp), daemon=False)
    thread.start()


if __name__ == "__main__":
    main()
