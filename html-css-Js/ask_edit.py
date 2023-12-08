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
    print(f"Section: {section['description']}\n")
    for feature in section['features']:
        print(f"  - {feature}")
    print("\n" + "-" * 40 + "\n")

def main():
    # Load the TOML data from an external file
    file_path = 'your_external_file.toml'  # Replace with the path to your TOML file
    with open(file_path, 'r') as file:
        data_dict = toml.load(file)

    # Print sections
    for section_key in data_dict:
        section = data_dict[section_key]
        if not wait_for_enter_or_escape():
            sys.exit()
        print_section(section)

if __name__ == "__main__":
    main()
