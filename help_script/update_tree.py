import os
import argparse
from pathlib import Path

def generate_project_tree(start_path: str) -> str:
    tree_lines = []
    start_path = Path(start_path)
    
    ignore_dirs = {'.git', '__pycache__', '.pytest_cache', 'venv', 'env', 'node_modules', '.idea', '.vscode', 'help_scripts'}
    ignore_files = {'.DS_Store', '.gitignore', '.env', 'Thumbs.db'}
    
    def add_directory(path: Path, prefix: str = "", is_last: bool = True):
        connector = "└── " if is_last else "├── "
        tree_lines.append(f"{prefix}{connector}{path.name}/")
        
        new_prefix = prefix + ("    " if is_last else "│   ")
        
        try:
            items = sorted([item for item in path.iterdir()])
            
            items = [item for item in items 
                    if not (item.is_dir() and item.name in ignore_dirs) 
                    and not (item.is_file() and item.name in ignore_files)]
            
            dirs = [item for item in items if item.is_dir()]
            files = [item for item in items if item.is_file()]
            sorted_items = dirs + files
            
            for i, item in enumerate(sorted_items):
                is_last_item = i == len(sorted_items) - 1
                
                if item.is_dir():
                    add_directory(item, new_prefix, is_last_item)
                else:
                    connector = "└── " if is_last_item else "├── "
                    tree_lines.append(f"{new_prefix}{connector}{item.name}")
                    
        except PermissionError:
            tree_lines.append(f"{new_prefix}└── [Permission denied]")
    
    tree_lines.append(f"{start_path.name}/")
    add_directory(start_path, "", True)
    
    return "\n".join(tree_lines)

def update_readme_with_tree(readme_path: str, project_tree: str, marker: str = "## Project Structure") -> bool:
    if not os.path.exists(readme_path):
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(f"# Project\n\n{marker}\n\n```\n{project_tree}\n```\n")
        return True
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if marker in content:
        lines = content.split('\n')
        new_lines = []
        skip_section = False
        
        for line in lines:
            if marker in line:
                skip_section = True
                new_lines.append(line)
                new_lines.append('')
                new_lines.append('```')
                new_lines.append(project_tree)
                new_lines.append('```')
            elif skip_section and line.strip() == '```':
                continue
            elif skip_section and not line.strip().startswith('```'):
                skip_section = False
                if line.strip():
                    new_lines.append(line)
            elif not skip_section:
                new_lines.append(line)
        
        new_content = '\n'.join(new_lines)
    else:
        new_content = content + f"\n\n{marker}\n\n```\n{project_tree}\n```\n"
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def main():
    parser = argparse.ArgumentParser(description='Update project tree in README.md')
    parser.add_argument('--path', '-p', default='..', help='Project root path')
    parser.add_argument('--readme', '-r', default='../README.md', help='README file name')
    parser.add_argument('--marker', '-m', default='## Project Structure', help='Marker to find/replace tree section')
    
    args = parser.parse_args()
    
    project_tree = generate_project_tree(args.path)
    
    readme_path = os.path.join(args.path, args.readme) if args.readme.startswith('/') else args.readme
    success = update_readme_with_tree(readme_path, project_tree, args.marker)
    
    if success:
        print(f"✅ Project tree successfully updated in {readme_path}")
        print(f"\nGenerated tree:\n")
        print(project_tree)
    else:
        print("❌ Failed to update README")

if __name__ == "__main__":
    main()