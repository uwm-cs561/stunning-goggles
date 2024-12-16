import os
import json


def get_relative_path(filename):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dir_path, filename)


def load_results(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    return [json.loads(line) for line in lines if line != ""]


## metrics of interest:
# percent zeros
def get_num_zeros(results, tolerance=1e-2):
    return sum(
        1 if result["bleu"] < tolerance else 0 for result in results if "bleu" in result
    )


# percent errors
def get_num_errors(results):
    return sum(1 if "error" in result else 0 for result in results)


# some kind of plot of the non-zeros
def get_non_zeros(results, tolerance=1e-2):
    return [
        result["bleu"]
        for result in results
        if "bleu" in result and result["bleu"] >= tolerance
    ]


# plot of deltas, w/ summary statistics
def get_deltas(baseline_results, manipulation_results, tolerance=1e-4):
    return_val = []
    for baseline_result, manip_result in zip(baseline_results, manipulation_results):
        if "error" in baseline_result or "error" in manip_result:
            return_val.append(None)
            continue

        return_val.append(manip_result["bleu"] - baseline_result["bleu"])
    return return_val


if __name__ == "__main__":
    base_results_data = load_results(get_relative_path("_base.jsonl"))
    print(get_num_errors(base_results_data))
    print(get_num_zeros(base_results_data))
