import toml
import sys

def print_section(section):
    print(f"Section: {section['name']}\n")
    print(section['content'])
    print("\n" + "-" * 40 + "\n")

def wait_for_enter_or_escape():
    print("Press Enter to load the next section. Press ESC to terminate.")
    user_input = input()
    return user_input.lower() != 'esc'

def main():
    # Load the TOML data
    with open('your_file_path_here.toml', 'r') as file:
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

