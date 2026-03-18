import sys
from planner.classifier import classify
from planner.generator import generate
from executor.actions import write_file, read_file
from logger import log_event

def main() -> None:
    if len(sys.argv) < 2:
        print('Usage: python3 main.py "your task here"')
        raise SystemExit(1)

    user_input = " ".join(sys.argv[1:])
    result = classify(user_input)

    print("CLASSIFIER:")
    print(result)

    if result["clarification_needed"]:
        print("\nCLARIFICATION NEEDED:")
        print(result["clarification_question"])
        log_event(user_input, result["action"], result["confidence"], "clarification_needed")
        return

    payload = generate(user_input, result["action"])
    print("\nGENERATOR:")
    print(payload)

    try:
        if result["action"] == "read_file":
            output = read_file(payload["filename"])
            print(output)
            log_event(user_input, result["action"], result["confidence"], "ok")
            return

        if result["action"] == "write_file":
            output = write_file(payload["filename"], payload["content"])
            print(output)
            log_event(user_input, result["action"], result["confidence"], "ok")
            return

        print("\nNo supported action.")
        log_event(user_input, result["action"], result["confidence"], "unsupported")

    except ValueError as e:
        print(f"\nERROR: {e}")
        log_event(user_input, result["action"], result["confidence"], f"error: {e}")

if __name__ == "__main__":
    main()
