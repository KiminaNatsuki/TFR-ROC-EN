import os
import re
from pathlib import Path

def fix_indentation():
    script_dir = Path(__file__).parent.resolve()
    
    loc_dirs = [
        script_dir / 'localisation' / 'simp_chinese',
        script_dir / 'localisation' / 'english'
    ]
    
    fixed_files_count = 0
    fixed_lines_count = 0
    
    for loc_dir in loc_dirs:
        for root, dirs, files in os.walk(loc_dir):
            for filename in files:
                if not filename.endswith('.yml'):
                    continue
                    
                file_path = Path(root) / filename
                
                with open(file_path, 'r', encoding='utf-8-sig') as f:
                    lines = f.readlines()
                    
                new_lines = []
                file_changed = False
                for line in lines:
                    # If it's a root node, keep it as is
                    if re.match(r'^l_(simp_chinese|english):', line):
                        new_lines.append(line)
                        continue
                        
                    # Ignore empty lines or comments
                    if not line.strip() or line.lstrip().startswith('#'):
                        new_lines.append(line)
                        continue
                        
                    # Check if the line has exactly one leading space
                    # Paradox format: [space]KEY: "VALUE"
                    # We want to force it to have exactly 1 space
                    # E.g. "VICTORY_POINTS_35: \"Västerås\"" -> " VICTORY_POINTS_35: \"Västerås\""
                    # E.g. "  VICTORY_POINTS_35: \"Västerås\"" -> " VICTORY_POINTS_35: \"Västerås\""
                    match = re.match(r'^(\s*)([\w\.\-]+)(:\d*\s*".*".*)$', line)
                    if match:
                        indent = match.group(1)
                        key = match.group(2)
                        rest = match.group(3)
                        
                        if indent != " ":
                            line = f' {key}{rest}\n'
                            file_changed = True
                            fixed_lines_count += 1
                    
                    new_lines.append(line)
                    
                if file_changed:
                    with open(file_path, 'w', encoding='utf-8-sig') as f:
                        f.writelines(new_lines)
                    fixed_files_count += 1
                    
    print(f"Fixed indentation in {fixed_files_count} files ({fixed_lines_count} lines fixed).")

if __name__ == '__main__':
    fix_indentation()
