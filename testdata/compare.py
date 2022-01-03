import sys
import json


def read_result_file(argv_index: int):
    with open(sys.argv[argv_index]) as f:
        return f.read()


def parse_result_content(content: str):
    objects = []
    current = []
    for line in content.splitlines():
        if line == "":
            continue

        if line[0] == "}":
            current.append(line)
            objects.append(json.loads("\n".join(current)))
            current = []

        if line[0] in "{ \t":
            current.append(line)

    return objects


def parse_results(argv_index: int):
    return parse_result_content(read_result_file(argv_index))


def compare_findings(a, b):
    if b is None:
        return a["data"] is None
    if a["result"] == b["result"]:
        return True
    return False


resa = parse_results(1)
resb = parse_results(2)
resb_dict = {}
for f in resb:
    rule_id = f["agent_rule_id"]
    resb_dict[rule_id] = f
    if rule_id == "cis-docker-1.2.0-2.1":
        print(f)

resb = {f["agent_rule_id"]: f for f in resb}

true_counter = 0
false_counter = 0
for finding in resa:
    rule_id = finding["agent_rule_id"]
    if rule_id == "cis-docker-1.2.0-2.1":
        print(finding)
    print(rule_id)
    against = resb_dict.get(rule_id)
    test = compare_findings(finding, against)
    print(test)
    if test:
        true_counter += 1
    else:
        print(finding)
        print(against)
        false_counter += 1
print(true_counter, false_counter)
