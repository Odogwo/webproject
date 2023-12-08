import toml
import keyboard

def print_section(section):
    print(f"Section: {section['name']}\n")
    print(section['content'])
    print("\n" + "-" * 40 + "\n")

def wait_for_enter_or_escape():
    while True:
        if keyboard.is_pressed('enter'):
            return True
        elif keyboard.is_pressed('esc'):
            return False

def main():
    # Load the TOML data
    with open('your_file_path_here.toml', 'r') as file:
        data = toml.load(file)

    # Print sections
    for section in data['sections']:
        print("Press Enter to load the next section. Press ESC to terminate.")
        if not wait_for_enter_or_escape():
            return
        print_section(section)

    # Print relationships
    for relationship in data['relationships']:
        print("Press Enter to load the next relationship. Press ESC to terminate.")
        if not wait_for_enter_or_escape():
            return
        print(f"Relationship: {relationship['name']}\n")
        print(relationship['description'])
        for section_name in relationship['sections']:
            section = next((s for s in data['sections'] if s['name'] == section_name), None)
            if section:
                print("Press Enter to load the next section. Press ESC to terminate.")
                if not wait_for_enter_or_escape():
                    return
                print_section(section)
        print("\n" + "=" * 40 + "\n")

if __name__ == "__main__":
    main()

