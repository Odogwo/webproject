import toml

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
        print_section(section)

    # Print relationships
    for relationship in data['relationships']:
        print(f"Relationship: {relationship['name']}\n")
        print(relationship['description'])
        for section_name in relationship['sections']:
            section = next((s for s in data['sections'] if s['name'] == section_name), None)
            if section:
                print_section(section)
        print("\n" + "=" * 40 + "\n")

if __name__ == "__main__":
    main()
