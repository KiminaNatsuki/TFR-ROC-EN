import os
import subprocess
import re
from pathlib import Path

def restore_lost_translations():
    script_dir = Path(__file__).parent.resolve()
    english_dir = script_dir / 'localisation' / 'english'

    for root, dirs, files in os.walk(english_dir):
        for filename in files:
            if not filename.endswith('.yml'):
                continue
                
            file_path = Path(root) / filename
            rel_path = file_path.relative_to(script_dir).as_posix()
            
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                current_lines = f.readlines()
                
            try:
                result = subprocess.run(
                    ['git', 'show', f'ed6680d:{rel_path}'],
                    cwd=str(script_dir),
                    capture_output=True,
                    check=True
                )
                old_content = result.stdout.decode('utf-8-sig', errors='replace')
            except subprocess.CalledProcessError:
                continue
                
            old_translations = {}
            for line in old_content.splitlines():
                match = re.match(r'^\s*([\w\.\-]+)(?::\d+)?\s*:\s*\"(.*)\"', line)
                if not match:
                    match = re.match(r'^\s*([\w\.\-]+)(?::\d+)?\s+\"(.*)\"', line)
                if not match:
                    match = re.match(r'^\s*([\w\.\-]+)(?::\d+)?\s*:\s*\"(.*)\"', line)
                    
                if match:
                    key = match.group(1)
                    val = match.group(2)
                    if re.search(r'[a-zA-Z]', val):  # Has English letters
                        old_translations[key] = val
                        
            if not old_translations:
                continue
                
            new_lines = []
            replaced_count = 0
            for line in current_lines:
                match = re.match(r'^(\s*)([\w\.\-]+)((?::\d+)?\s*:\s*\")(.*)(\")', line)
                if not match:
                    match = re.match(r'^(\s*)([\w\.\-]+)((?::\d+)?\s+\")(.*)(\")', line)
                    
                if match:
                    indent = match.group(1)
                    key = match.group(2)
                    colon_part = match.group(3)
                    current_val = match.group(4)
                    end_quote = match.group(5)
                    
                    if key in old_translations and not re.search(r'[a-zA-Z]{2}', current_val):
                        line = f'{indent}{key}{colon_part}{old_translations[key]}{end_quote}\n'
                        replaced_count += 1
                new_lines.append(line)
                
            if replaced_count > 0:
                with open(file_path, 'w', encoding='utf-8-sig') as f:
                    f.writelines(new_lines)
                print(f"Restored {replaced_count} translations in {filename}")

if __name__ == '__main__':
    restore_lost_translations()
