import os

# File tree as a multi-line string
file_tree = """
my_project/
│
├── main.py  # Entry point of the application
├── README.md
├── config.py  # Configuration settings
│
├── gui/
│   ├── __init__.py
│   ├── main_window.py  # Main application window setup
│   │
│   ├── components/  # Reusable GUI components
│   │   ├── __init__.py
│   │   ├── navigation_panel.py
│   │   ├── status_bar.py
│   │   └── custom_button.py
│   │
│   ├── forms/  # Different forms or complex GUI sections
│   │   ├── __init__.py
│   │   ├── login_form.py
│   │   ├── settings_form.py
│   │   └── user_profile_form.py
│   │
├── assets/
│   ├── icons/
│   ├── images/
│   └── sounds/
│
├── lib/
│   ├── __init__.py
│   ├── database_manager.py
│   └── network_utils.py
│
└── tests/
    ├── __init__.py
    ├── test_main_window.py
    └── components/
        ├── __init__.py
        ├── test_navigation_panel.py
        └── test_custom_button.py
"""

# Configuration map for parsing characters
parse_map = {
    'branch': '├──',
    'leaf': '└──',
    'indentation': '    ',  # 4 spaces
    'directory_mark': '/'
}

import os

# Configuration map for parsing characters
parse_map = {
    'branch': '├──',
    'leaf': '└──',
    'indentation': '    ',  # 4 spaces
    'directory_mark': '/'
}


def check_structure(tree, config):
    current_path = []
    lines = tree.strip().split('\n')
    root_detected = False

    for line in lines:
        # Handle the root directory separately if not already detected
        if not root_detected and '/' in line:
            name = line.strip().replace('/', '')
            current_path = [name]
            print(f"Directory to create: {current_path[0]}/")
            root_detected = True
            continue

        depth = line.find(config['branch']) if config['branch'] in line else line.find(config['leaf'])
        if depth == -1:
            continue
        depth //= len(config['indentation'])  # Each level of indentation defined in the config
        name = line.strip(f"{config['branch']} {config['leaf']}│\n ")
        if '#' in name:  # Remove comments from filenames and directory names
            name = name.split('#')[0].strip()
        current_path = current_path[:depth] + [name]
        path = '/'.join(current_path).replace('//', '/')  # Correct redundant slashes
        if path.endswith(config['directory_mark']):
            print(f"Directory to create: {path}")
        else:
            print(f"File to create: {path}")


def parse_and_create_structure(tree, config, dry_run=False):
    if dry_run:
        check_structure(tree, config)
        return

    current_path = []
    lines = tree.strip().split('\n')
    root_detected = False

    for line in lines:
        if not root_detected and '/' in line:
            name = line.strip().replace('/', '')
            current_path = [name]
            if dry_run:
                print(f"Directory to create: {current_path[0]}/")
            else:
                os.makedirs(current_path[0], exist_ok=True)
            root_detected = True
            continue

        depth = line.find(config['branch']) if config['branch'] in line else line.find(config['leaf'])
        if depth == -1:
            continue
        depth //= len(config['indentation'])
        name = line.strip(f"{config['branch']} {config['leaf']}│\n ")
        if '#' in name:  # Remove comments
            name = name.split('#')[0].strip()
        current_path = current_path[:depth] + [name]
        path = '/'.join(current_path).replace('//', '/')  # Correct redundant slashes
        if path.endswith(config['directory_mark']):
            if not dry_run:
                os.makedirs(path, exist_ok=True)
        else:
            if not dry_run:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                open(path, 'w').close()


# Call the function with dry_run set to True to check the structure without making changes
parse_and_create_structure(file_tree, parse_map, dry_run=True)
