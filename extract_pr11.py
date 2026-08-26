import os
import re
import subprocess

def run_cmd(cmd):
    subprocess.run(cmd, check=True, shell=True)

# 1. Checkout pr-11 and extract all translations
print("Checking out pr-11...")
run_cmd("git checkout pr-11")

pr_dict = {}
en_dir = r"localisation\english"
for root, dirs, files in os.walk(en_dir):
    for file in files:
        if file.endswith('.yml'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8-sig') as f:
                for line in f:
                    match = re.match(r'^\s*([\w_\.]+)(?::\d*)?\s*"(.*)"\s*$', line)
                    if match:
                        pr_dict[match.group(1)] = match.group(2)

print(f"Extracted {len(pr_dict)} strings from pr-11.")

# 2. Checkout main
print("Checking out main...")
run_cmd("git checkout main")

# 3. Extract Chinese source text
chi_dict = {}
chi_dir = r"..\TFR-ROC\localisation\simp_chinese"
for root, dirs, files in os.walk(chi_dir):
    for file in files:
        if file.endswith('.yml'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8-sig') as f:
                for line in f:
                    match = re.match(r'^\s*([\w_\.]+)(?::\d*)?\s*"(.*)"\s*$', line)
                    if match:
                        chi_dict[match.group(1)] = match.group(2)

print(f"Extracted {len(chi_dict)} strings from Chinese source.")

def strip_punct(s):
    return re.sub(r'[\W_]+', '', s)

# 4. Inject valid translations into main
replaced_count = 0
for root, dirs, files in os.walk(en_dir):
    for file in files:
        if file.endswith('.yml'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8-sig') as f:
                lines = f.readlines()
            
            changed = False
            new_lines = []
            for line in lines:
                match = re.match(r'^(\s*)([\w_\.]+)(:\d*\s*")(.+)("\s*)$', line)
                if not match:
                    match = re.match(r'^(\s*)([\w_\.]+)(:\d*\s*")()("\s*)$', line)
                    
                if match:
                    indent = match.group(1)
                    key = match.group(2)
                    colon = match.group(3)
                    current_val = match.group(4)
                    end_quote = match.group(5)
                    
                    if key in pr_dict:
                        pr_val = pr_dict[key]
                        chi_val = chi_dict.get(key, '')
                        
                        # Conditions to take the PR translation:
                        # 1. PR val has English letters
                        # 2. PR val != current val
                        # 3. PR val != Chinese source (ignoring punct)
                        
                        has_english = bool(re.search(r'[a-zA-Z]', pr_val))
                        is_different = pr_val != current_val
                        is_not_chinese = strip_punct(pr_val) != strip_punct(chi_val)
                        
                        if has_english and is_different and is_not_chinese:
                            line = f"{indent}{key}{colon}{pr_val}{end_quote}\n"
                            changed = True
                            replaced_count += 1
                            
                new_lines.append(line)
                
            if changed:
                with open(filepath, 'w', encoding='utf-8-sig') as f:
                    f.writelines(new_lines)

print(f"Successfully injected {replaced_count} new valid translations from PR 11 into main!")
