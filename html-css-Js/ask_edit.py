import toml
import sys

try:
    import msvcrt

    def wait_for_enter_or_escape():
        print("Press Enter to load the next section. Press ESC to terminate.")
        while True:
            key = msvcrt.getch()
            if key == b'\r':  # Enter key
                return True
            elif key == b'\x1b':  # ESC key
                return False

except ImportError:
    # For non-Windows systems, use a simple input prompt
    def wait_for_enter_or_escape():
        print("Press Enter to load the next section. Press Enter again to terminate.")
        input()
        return True

def print_section(section):
    print(f"Section: {section['name']}\n")
    print(section['content'])
    print("\n" + "-" * 40 + "\n")

def main():
    # Load the TOML data
    with open('introduction.toml', 'r') as file:
        data = toml.load(file)

    # Print sections
    for section in data['sections']:
        if not wait_for_enter_or_escape():
            sys.exit()
        print_section(section)

    # Print relationships
    for relationship in data['relationships']:
        if not wait_for_enter_or_escape():
            sys.exit()
        print(f"Relationship: {relationship['name']}\n")
        print(relationship['description'])
        for section_name in relationship['sections']:
            section = next((s for s in data['sections'] if s['name'] == section_name), None)
            if section:
                if not wait_for_enter_or_escape():
                    sys.exit()
                print_section(section)
        print("\n" + "=" * 40 + "\n")

if __name__ == "__main__":
    main()
