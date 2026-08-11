import os
import re
from pathlib import Path

def sync_keys():
    script_dir = Path(__file__).parent.resolve()
    simp_chinese_dir = script_dir / 'localisation' / 'simp_chinese'
    english_dir = script_dir / 'localisation' / 'english'
    
    # 1. Map base keys to exact colon formats
    base_keys = {}
    for root, dirs, files in os.walk(simp_chinese_dir):
        for file in files:
            if not file.endswith('.yml'): continue
            
            with open(Path(root) / file, 'r', encoding='utf-8-sig') as f:
                lines = f.readlines()
                
            for line in lines:
                # E.g. " ROC.1.t:0 \"text\""
                match = re.match(r'^(\s*)([\w\.\-]+)(:\d*\s*)(".*".*)$', line)
                if match:
                    key = match.group(2)
                    colon_part = match.group(3)
                    base_keys[key] = colon_part

    # 2. Apply exact colon formats to english files
    fixed_files = 0
    fixed_keys = 0
    
    for root, dirs, files in os.walk(english_dir):
        for file in files:
            if not file.endswith('.yml'): continue
            
            file_path = Path(root) / file
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                lines = f.readlines()
                
            new_lines = []
            changed = False
            for line in lines:
                match = re.match(r'^(\s*)([\w\.\-]+)(:\d*\s*)(".*".*)$', line)
                if match:
                    indent = match.group(1)
                    key = match.group(2)
                    current_colon = match.group(3)
                    rest = match.group(4)
                    
                    if key in base_keys:
                        correct_colon = base_keys[key]
                        if current_colon != correct_colon:
                            line = f'{indent}{key}{correct_colon}{rest}\n'
                            changed = True
                            fixed_keys += 1
                            
                new_lines.append(line)
                
            if changed:
                with open(file_path, 'w', encoding='utf-8-sig') as f:
                    f.writelines(new_lines)
                fixed_files += 1
                
    print(f"Fixed {fixed_keys} keys across {fixed_files} files to perfectly match Chinese base format.")

if __name__ == '__main__':
    sync_keys()
