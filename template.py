import os


def get_yes_no_input(prompt):
    """Get a yes/no response from the user with validation."""
    while True:
        response = input(f"{prompt} (y/n, default=n): ").strip().lower()
        if not response or response == 'n' or response == 'no':
            return False
        elif response == 'y' or response == 'yes':
            return True
        else:
            print("Invalid input. Please enter 'y' or 'n'.")


def create_directory(path):
    """Create directory if it doesn't exist."""
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Created directory: {path}")
        else:
            print(f"Directory already exists: {path}")
    except Exception as e:
        print(f"Error creating directory {path}: {e}")


def main():
    """Main function to create project structure."""
    cwd = os.getcwd()
    print("Creating project structure...")
    
    # Create base directories
    create_directory(os.path.join(cwd, 'src'))
    create_directory(os.path.join(cwd, 'tests'))
    create_directory(os.path.join(cwd, 'docs'))
    create_directory(os.path.join(cwd, 'scripts'))
    src = os.path.join(cwd, 'src')
    
    # Create core structure directories
    create_directory(os.path.join(src, 'di'))  # Dependency injection configurations
    create_directory(os.path.join(src, 'entrypoints'))  # External interfaces
    create_directory(os.path.join(src, 'usecases'))  # Application-specific business rules
    create_directory(os.path.join(src, 'models'))  # Domain entities
    create_directory(os.path.join(src, 'common'))  # Shared code and utilities
    create_directory(os.path.join(src, 'settings'))  # Configuration settings
    
    # Handle entrypoints directories
    entrypoints = os.path.join(src, 'entrypoints')
    if get_yes_no_input("Create GraphQL entrypoint?"):
        create_directory(os.path.join(entrypoints, 'graphql'))
    
    if get_yes_no_input("Create HTTP entrypoint?"):
        create_directory(os.path.join(entrypoints, 'http'))
    
    # Handle repositories directories
    repositories = os.path.join(src, 'repositories')
    create_directory(repositories)

    # Handle db directories in settings
    db = os.path.join(src, "settings", "db")
    
    if get_yes_no_input("Add support for Relational Database (e.g., SQLite, MySQL, PostgreSQL)?"):
        create_directory(os.path.join(repositories, 'relational_db'))
    
    if get_yes_no_input("Add support for Document Database (e.g., MongoDB, Cassandra)?"):
        create_directory(os.path.join(repositories, 'document_db'))
    
    if get_yes_no_input("Add support for Key-Value Database (e.g., Redis, Memcached)?"):
        create_directory(os.path.join(repositories, 'key_value_db'))
    
    print("Project structure created successfully!")


if __name__ == "__main__":
    main()


