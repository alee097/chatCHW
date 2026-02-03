from engine import evaluate

def run_tests():
    print("\n---------Running Automated Tests---------")
    
    test_rules = {
        "variables": ["fever", "cough"],
        "rules": [
            {"id": "R1", "when": "fever AND cough", "then": "FLU"},
            {"id": "R2", "when": "cough", "then": "COLD"}
        ],
        "default": "HEALTHY"
    }

    test_cases = [
        ({"id": "T1", "fever": True, "cough": True}, "FLU"),
        ({"id": "T2", "fever": False, "cough": True}, "COLD"),
        ({"id": "T3", "fever": False, "cough": False}, "HEALTHY")
    ]

    passed = True
    for patient, expected in test_cases:
        result = evaluate(test_rules, patient)
        
        if result and result["outcome"] == expected:
            print(f"Pass: Patient {patient['id']} -> {expected}")
        else:
            print(f"Fail: Patient {patient['id']} -> Expected {expected}, got {result.get('outcome')}")
            passed = False
            
    if passed:
        print("\nSuccess! All tests passed.")
    else:
        print("\nFailure. Some tests failed.")

if __name__ == "__main__":
    run_tests()
