import toml

def ask_question(section):
    print(section['content'])
    input("Press Enter to continue...")

def main():
    # Load the TOML data
    with open('your_file_path_here.toml', 'r') as file:
        data = toml.load(file)

    # Iterate through sections and ask questions
    for section_name in data['sections']:
        section = next((s for s in data['sections'] if s['name'] == section_name), None)
        if section:
            ask_question(section)

    # Ask questions related to relationships
    for relationship in data['relationships']:
        print(relationship['description'])
        for section_name in relationship['sections']:
            section = next((s for s in data['sections'] if s['name'] == section_name), None)
            if section:
                ask_question(section)

if __name__ == "__main__":
    main()
