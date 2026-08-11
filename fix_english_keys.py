import os
from pathlib import Path
import re

def prepare_for_crowdin():
    script_dir = Path(__file__).parent.resolve()
    english_dir = script_dir / 'localisation' / 'english'

    print(f"Fixing keys in English files in:\n  {english_dir}")
    
    for root, dirs, files in os.walk(english_dir):
        for file in files:
            if file.endswith('.yml'):
                file_path = Path(root) / file
                with open(file_path, 'r', encoding='utf-8-sig') as f:
                    lines = f.readlines()
                
                new_lines = []
                for line in lines:
                    # Strip the version number (e.g. :0 or :1) from the key
                    # Example:  ROC.1.t:0 "Text" ->  ROC.1.t: "Text"
                    if re.match(r'^\s*[\w\.\-]+:\d+\s+\"', line):
                        line = re.sub(r'(^\s*[\w\.\-]+):\d+(\s+\")', r'\1:\2', line)
                    
                    new_lines.append(line)
                
                with open(file_path, 'w', encoding='utf-8-sig') as f:
                    f.writelines(new_lines)
                
    print("\nKeys fixed! Files are now ready for Crowdin import.")

if __name__ == '__main__':
    prepare_for_crowdin()
