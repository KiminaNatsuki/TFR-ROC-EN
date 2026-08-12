import os
from pathlib import Path

def fix_l_english():
    script_dir = Path(__file__).parent.resolve()
    english_dir = script_dir / 'localisation' / 'english'
    
    fixed = 0
    for root, dirs, files in os.walk(english_dir):
        for file in files:
            if not file.endswith('.yml'): continue
            
            file_path = Path(root) / file
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                content = f.read()
                
            if 'l_simp_chinese:' in content:
                content = content.replace('l_simp_chinese:', 'l_english:')
                with open(file_path, 'w', encoding='utf-8-sig') as f:
                    f.write(content)
                fixed += 1
                
    print(f"Fixed {fixed} files to start with l_english:")

if __name__ == '__main__':
    fix_l_english()
