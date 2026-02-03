import json

def import_json(filename):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: {filename} was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: failed to parse JSON from {filename}.")
        return None
    
def import_jsonl(filename):
    data = []
    try:
        with open(filename, "r") as f:
            for line in f:
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
        return data
    except FileNotFoundError:
        print(f"Error: {filename} was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: failed to parse JSON from {filename}.")
        return None   

def interpret(input_ruleset):
    rules = input_ruleset["rules"]
    default = input_ruleset["default"]
    mermaid = ["flowchart TD"]
    start_rule_id = rules[0]["id"]
    mermaid.append(f" Start --> {start_rule_id}")

    for i, rule in enumerate(rules):
        current_rule_id = rule["id"]
        outcome = rule["then"]
        mermaid.append(f" {current_rule_id} --> |Yes| {outcome}")
        if i < (len(rules) - 1):
            next_rule_id = rules[i + 1]["id"]
            mermaid.append(f" {current_rule_id} --> |No| {next_rule_id}")
        else:
            mermaid.append(f" {current_rule_id} --> |No| {default}")
    return "\n".join(mermaid)

def evaluate(input_ruleset, input_patient): #takes in one line of jsonl input_patients
    rules = input_ruleset["rules"]
    default = input_ruleset["default"]
    variables = set(input_ruleset.get("variables", []))
    valid = {"and", "or", "not", "true", "false"}
    path = []

    for rule in rules:
        rule_id = rule["id"]
        condition = rule["when"].replace("(", " ").replace(")", " ")
        words = condition.split()
        for word in words:
            if word.lower() not in valid and word.lower() not in variables:
                if variables:
                    print(f"Error: {rule_id} contains invalid variable {word}.")
                    return None
            if word.lower() in variables and word.lower() not in input_patient:
                print(f"Error: {rule_id} requires unknown variable {word}.")
                return None

        condition = rule["when"].replace("AND", "and").replace("OR","or").replace("NOT", "not")
        evidence = rule.get("evidence", "N/A")

        try:
            status = eval(condition, {}, input_patient)
        except Exception:
            print(f"Runtime/syntax error in {rule_id}.")
            status = False
        path.append(f"{rule_id}: {status}")

        if status:
            return {
                "patient_id": input_patient.get("id"),
                "outcome": rule["then"],
                "matched_rule": rule_id,
                "path": path,
                "justification": f"{rule_id} ({rule['when']}) was found to be True.",
                "evidence": evidence,
            }
    else:
        return {
            "patient_id": input_patient.get("id"),
            "outcome": default,
            "matched_rule": "None",
            "path": path,
            "justification": "No rule was found to be True.",
            "evidence": "N/A",        
    }

def reconstruct(input_manual):
    new_ruleset = {"rules": [], "default": None}
    rule_num = 1
    for rule in input_manual:
        chunk_id = rule["chunk_id"]
        text = rule["text"]

        if "Otherwise" in text:
            string = text.split("classify as ")
            outcome = string[1].strip(".")
            new_ruleset["default"] = outcome
            continue
        if "classify as" in text:
            string = text.split(", classify as ")
            condition = string[0].replace("If ", "").strip()
            condition = condition.replace(" is true", "")
            outcome = string[1].strip(".")
            
            new_ruleset["rules"].append({
                "id": f"R{rule_num}",
                "when": condition,
                "then": outcome,
                "evidence": f"{chunk_id}"
            })
            rule_num += 1
    return new_ruleset

if __name__ == "__main__":
    sample_ruleset = import_json("sample_data/sample_ruleset.json")
    sample_patients = import_jsonl("sample_data/sample_patients.jsonl")
    sample_excerpt = import_jsonl("sample_data/sample_manual_excerpt.jsonl")

    print("-----------------Mermaid-----------------\n")
    print(interpret(sample_ruleset))

    print("\n-------Manual Excerpts --> Ruleset-------\n")
    output = reconstruct(sample_excerpt)
    print(json.dumps(output))

    print("\n-------------Patient Outputs-------------\n")
    reconstructed = reconstruct(sample_excerpt)
    for p in sample_patients:
        output = evaluate(reconstructed, p)
        print(json.dumps(output))
    print("\n")