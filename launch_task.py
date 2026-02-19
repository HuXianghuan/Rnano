import json
import random
import uuid
from multiprocessing import Pool
from typing import Type

import file_tools
from nanoparticles_pack.snowflake import *



def single_task(siRNA, hairpin, kissloop, shape_cls, substitute_ratio, constraints, gc_clasp_length, overhang_length):

    try:
        np = shape_cls(gc_clasp_length=gc_clasp_length, overhang_length=overhang_length)
        pool_requirements = shape_cls().count_elements()
        sirna_requirement = pool_requirements[SenseSirna]
        hairpin_requirement = pool_requirements[HairpinLoop]
        kissloop_requirement = pool_requirements[KissingLoop] // 2

        np.siRNA_list = select_with_coverage(siRNA, k=sirna_requirement)
        np.hairpin_list = select_with_coverage(hairpin, k=hairpin_requirement)
        np.kisspair_list = select_with_coverage(kissloop, k=kissloop_requirement)

        np.render_sequence()
        np.base_substitution(ratio=substitute_ratio, target=AntiSenseSirna)
        np.rnafold_testify()

        result = {
            "siRNAList": getattr(np, "siRNA_list", None),
            "hairpinList": getattr(np, "hairpin_list", None),
            "kisspairList": getattr(np, "kisspair_list", None),
            "sequence": getattr(np, "sequence", None),
            "secondStructure": getattr(np, "ss", None),
            "minimumFreeEnergy": getattr(np, "mfe", None),
            "mfeFrequency": getattr(np, "frequency", None),
            "mfeDiversity": getattr(np, "diversity", None)
        }

        if check_constraints(result=result, constraints=constraints):
            return result
        else:
            return None
    except ValueError:
        return None



def launch_task_mp(
        sirna_path,
        shape: Type[Snowflake],
        quantity,
        constraints=None,
        substitute_ratio=0,
        max_quantity=100,
        gc_clasp_length=1,
        overhang_length=2,
        output_format="json",
        output_filename="output",
        structural_elements_json_path="./default_seqs/default.json",
        n_processes=8,
        timestamp=None,
):
    default_elements = file_tools.read_json(file_path=structural_elements_json_path)

    siRNA = file_tools.read_fasta(file_path=sirna_path)
    hairpin = default_elements["hairPinLoop"]
    kissloop = default_elements["kissingLoop"]
    results = []

    total_count = 0


    with Pool(processes=n_processes) as pool:
        while len(results) < quantity and total_count < max_quantity:
            tasks_to_run = min(n_processes, quantity - len(results), max_quantity-total_count)
            total_count += tasks_to_run

            async_results = [
                pool.apply_async(
                    single_task,
                    args=(siRNA, hairpin, kissloop, shape, substitute_ratio, constraints, gc_clasp_length, overhang_length)
                )
                for _ in range(tasks_to_run)
            ]

            for ar in async_results:
                res = ar.get()
                if res:
                    results.append(res)
                    # print("valid result")
                else:
                    # print("invalid result")
                    pass


        if not results:
            raise Exception("No valid results")

        json_results = json.dumps(results, indent=2)

        workdir = file_tools.create_time_folder_with_timestamp(base_path="./tasks", timestamp=timestamp)
        output_filepath = file_tools.format_transfer(json_str=json_results, workdir=workdir, filename=output_filename, format=output_format)

        return output_filepath


def launch_task(
        sirna_path,
        shape: Type[Snowflake],
        quantity,
        constraints=None,
        substitute_ratio=0,
        max_quantity=100,
        gc_clasp_length=None,
        overhang_length=None,
        output_format="json",
        output_filename="output",
        structural_elements_json_path="./default_seqs/default.json",
        thread=8
):
    default_elements = file_tools.read_json(file_path=structural_elements_json_path)

    siRNA = file_tools.read_fasta(file_path=sirna_path)
    hairpin = default_elements["hairPinLoop"]
    kissloop = default_elements["kissingLoop"]

    pool_requirements = shape().count_elements()
    sirna_requirement = pool_requirements[SenseSirna]
    hairpin_requirement = pool_requirements[HairpinLoop]
    kissloop_requirement = pool_requirements[KissingLoop] // 2

    results = []

    total_count = 0
    success_count = 0

    while success_count < quantity and success_count < max_quantity:

        if total_count >= max_quantity:
            break
        else:
            total_count += 1



        np = shape(gc_clasp_length=gc_clasp_length, overhang_length=overhang_length)
        np.siRNA_list = select_with_coverage(siRNA, k=sirna_requirement)
        np.hairpin_list = select_with_coverage(hairpin, k=hairpin_requirement)
        np.kisspair_list = select_with_coverage(kissloop, k=kissloop_requirement)



        try:
            np.render_sequence()
            np.base_substitution(ratio=substitute_ratio, target=AntiSenseSirna)
            np.rnafold_testify()




            result = {
                "siRNAList": getattr(np, "siRNA_list", None),
                "hairpinList": getattr(np, "hairpin_list", None),
                "kisspairList": getattr(np, "kisspair_list", None),
                "sequence": getattr(np, "sequence", None),
                "secondStructure": getattr(np, "ss", None),
                "minimumFreeEnergy": getattr(np, "mfe", None),
                "mfeFrequency": getattr(np, "frequency", None),
                "mfeDiversity": getattr(np, "diversity", None)
            }



            if check_constraints(result=result, constraints=constraints):
                success_count += 1
                results.append(result)
                print("valid result")
            else:
                print("not fit constraints")
                continue

        except ValueError:
            print("wrong ss")
            continue

    if not results:
        raise ValueError("no valid results")

    json_results = json.dumps(results, indent=2)


    workdir = file_tools.create_time_folder()
    output_filepath = file_tools.format_transfer(json_str=json_results, workdir=workdir, filename=output_filename, format=output_format)


    return output_filepath



def check_constraints(result: dict, constraints:dict) -> bool:
    if not constraints:
        return True
    for key, rule in constraints.items():
        value = result.get(key)
        if value is None:
            return False
        if "min" in rule and value < rule["min"]:
            return False
        if "max" in rule and value > rule["max"]:
            return False
    return True

def select_with_coverage(pool, k):
    if k <= len(pool):
        return random.sample(pool, k=k)
    else:
        result = random.sample(pool, k=len(pool))
        extra = random.choices(pool, k=k-len(pool))
        result.extend(extra)
        return result


if __name__ == "__main__":
    # a = create_time_folder()
    # print(a.resolve())
    #
    # file_tools.remove_folder(a)

    constraints = {
        "minimumFreeEnergy": {},
        "mfeFrequency": {"min": 0},
        "mfeDiversity": {"max": 5}
    }

    launch_task_mp(sirna_path="../sirna.fasta", shape=Triangle, quantity=10, output_format="json", constraints=constraints)
