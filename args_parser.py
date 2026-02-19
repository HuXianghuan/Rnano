# args_parser.py
import argparse

def build_parser():
    # --- 父 parser，存放通用参数 ---
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument("-s", "--sirna-path", type=str, required=True)
    common_parser.add_argument("-q", "--quantity", type=int, default=10)
    common_parser.add_argument("-m", "--max-quantity", type=int, default=100)
    common_parser.add_argument("-r", "--substitute-ratio", type=float, default=0)
    common_parser.add_argument("-p", "--processes", type=int, default=8)
    common_parser.add_argument("-f", "--output-format", choices=["json","csv"], default="json")
    common_parser.add_argument("-o", "--output-filename", default="output")

    # 约束参数
    common_parser.add_argument("--min-mfe", "-minmfe", type=float)
    common_parser.add_argument("--max-mfe", "-maxmfe", type=float)
    common_parser.add_argument("--min-mfe-frequency", "-minfreq", type=float)
    common_parser.add_argument("--max-mfe-frequency", "-maxfreq", type=float)
    common_parser.add_argument("--min-mfe-diversity", "-mindiv", type=float)
    common_parser.add_argument("--max-mfe-diversity", "-maxdiv", type=float)

    # --- 主 parser 和子命令 ---
    parser = argparse.ArgumentParser(description="Rnano Designer")
    subparsers = parser.add_subparsers(dest="shape", required=True)

    from nanoparticles_pack.snowflake import Triangle, Square, Pentagon, Hexagon
    from nanoparticles_pack.others import ThreeWayJunction

    shapes = ["triangle", "square", "pentagon", "hexagon", "3wj"]
    for shape in shapes:
        sp = subparsers.add_parser(shape, parents=[common_parser])
        sp.add_argument("--gc-clasp-length", "-g", type=int)
        sp.add_argument("--overhang-length", "-v", type=int)

    return parser
