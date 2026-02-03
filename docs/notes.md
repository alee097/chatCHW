Take-home Interview Notes

Functions:
1. Takes in DMN-style ruleset (JSON), turns it into a decision graph/Mermaid flowchart
2. Takes patient info (bool inputs), then runs them through decision graph
3. Takes text statement as input and translates it into ruleset, also returns which line of text produced each rule

Problem:
- CHWs can follow written manuals/text to make decisions, but machines can't. Need a way to turn these written manuals into a format that machines can deterministically execute the same way as humans.
- Mobile app with some AI implementation

Decision Model and Notation
- For each rule, if true -> return an outcome
- Block of rules evaluated from top to bottom
- If no rules return -> default outcome

Decision Graph
- Model to represent above
- For each rule, if true -> return an outcome. if not true -> check other rule
- If none return -> default outcome
- if/elif/else structure
- Clinical guides are often structured this way

Mermaid
- Takes text (format below) and turns into visual flowchart:
flowchart TD
 Start → R1
 R1 → |Yes| SEVERE
 R1 → |No| R2
- Helps with visualization and verification

Key Points:
- Must be deterministic, all of this takes place pre RAG
- Rules and diagram are absolutely accurate
- Must behave exactly as a clinical manual would evaluate

Design Approaches:
- Import and parse individual JSON files
- JSON and JSONL files separately, JSONLs need to be read line by line
- Note: JSONs are just formatted Python dictionaries, indexable and iterable
- Three separate functions: interpreter(), evaluator(), and translator()
- interpret(): takes in input ruleset, parses each rule in rule field and converts into Mermaid text, interpreting JSON rules and default case as a cohesive top-to-bottom flowchart
- Start with starting line, then line by line, if yes, point to outcome 1. If no, point to next rule id, but this requires there to be a valid next rule to add as next pointer. Once there is no valid next rule, aka once hits last line/max range, point to default outcome, and Mermaid flowchart is complete.
- evaluate(): takes in input ruleset and input patients, starting from beginning of ruleset, search each patient for matching rule, then condition, and corresponding condition in patients JSON/dict, if true, take path, if false, continue. return outcome as evaluated. remember to keep track of path: patient, rules, and whether evaluated true or false for each as run, to refer to as verification.
- needs to split input and verify valid variables, keywords, filter out typos, and that patients have all variables
- translate condition into evaluatable python code with bools
- output also needs to include evidence field, defined by reconstruct()
- reconstruct(): takes in text input, parses and translates into ruleset. As it parses, add evidence field to each rule, providing the assigned chunk id that can be referenced upon eval --> true. If not true, evidence --> N/A.
- Run all functions, include headers for each output section to make more readable.
- Flowchart, patient outputs with proof of evidence, ruleset from manual

References:
https://www.geeksforgeeks.org/python/read-json-file-using-python/
https://www.geeksforgeeks.org/python/enumerate-in-python/
https://www.w3schools.com/python/ref_func_eval.asp
https://www.w3schools.com/python/ref_string_replace.asp
https://www.geeksforgeeks.org/python/python-set-function/
https://mermaid.live
