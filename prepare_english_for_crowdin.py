import os
from pathlib import Path
import re

def prepare_for_crowdin():
    # Paths
    script_dir = Path(__file__).parent.resolve()
    english_dir = script_dir / 'localisation' / 'english'

    if not english_dir.exists():
        print(f"Error: Could not find English directory at {english_dir}")
        return

    print(f"Preparing English files in:\n  {english_dir}")
    
    for root, dirs, files in os.walk(english_dir):
        for file in files:
            if file.endswith('.yml'):
                file_path = Path(root) / file
                with open(file_path, 'r', encoding='utf-8-sig') as f:
                    lines = f.readlines()
                
                new_lines = []
                for line in lines:
                    # Skip untranslated strings so Crowdin marks them as empty/untranslated
                    if '[UNTRANSLATED]' in line:
                        continue
                    
                    # Replace l_english with l_simp_chinese so Crowdin can match the root key with the source files
                    if line.strip().startswith('l_english:'):
                        line = line.replace('l_english:', 'l_simp_chinese:')
                    
                    new_lines.append(line)
                
                with open(file_path, 'w', encoding='utf-8-sig') as f:
                    f.writelines(new_lines)
                
    print("\nPreparation complete! Files have been updated.")
    print("You can now commit and push the changes.")

if __name__ == '__main__':
    prepare_for_crowdin()
