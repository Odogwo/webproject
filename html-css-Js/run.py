import toml
import sys

try:
    import msvcrt

    def wait_for_enter_or_escape():
        print("Press Enter to show the answer. Press ESC to terminate.")
        while True:
            key = msvcrt.getch()
            if key == b'\r':  # Enter key
                return True
            elif key == b'\x1b':  # ESC key
                return False

except ImportError:
    # For non-Windows systems, use a simple input prompt
    def wait_for_enter_or_escape():
        print("Press Enter to show the answer. Press Enter again to terminate.")
        input()
        return True

def display_question(question):
    print(f"Question: {question['question']}")
    if not wait_for_enter_or_escape():
        sys.exit()
    print(f"Answer: {question['answer']}\n" + "=" * 40 + "\n")

def main():
    # Load the TOML data from an external file
    file_path = 'introduction.toml'  # Replace with the actual path to your TOML file
    with open(file_path, 'r') as file:
        data = toml.load(file)

    # Display questions and answers
    for question in data['questions']:
        display_question(question)

if __name__ == "__main__":
    main()
