import sys
import json
from collections import defaultdict


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
    findings = parse_result_content(read_result_file(argv_index))
    res = defaultdict(list)
    for finding in findings:
        rule_id = finding["agent_rule_id"]
        res[rule_id].append(finding)
    return res


def compare_simple_findings(a, b):
    if b is None:
        if a["data"] is None:
            return "ok"
        else:
            return "missing finding"
    if a["result"] == b["result"]:
        return "ok"
    return "different finding"


def compare_findings(a, b):
    if len(a) == 1:
        if b is None or len(b) == 0:
            return "missing finding"
        if len(b) == 1:
            return compare_simple_findings(a[0], b[0])
    else:
        print(a)
        print(b)
        return "investigate"


resa = parse_results(1)
resb = parse_results(2)

for rule_id, findings in resa.items():
    if rule_id == "cis-docker-1.2.0-4.1":
        print(findings)
    # print(rule_id, len(findings))
    print(rule_id)
    print(compare_findings(findings, resb.get(rule_id)))
