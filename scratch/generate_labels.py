import os
import json
import re

md_files = [
    "notebooks/01_data_understanding/rech0_hogar/decisiones-de-limpieza-not-drops.md",
    "notebooks/01_data_understanding/rech1_roster/decisiones-de-limpieza-not-drops.md",
    "notebooks/01_data_understanding/rech23_geografia/decisiones-de-limpieza-not-drops.md",
    "notebooks/01_data_understanding/rech6_antropometria/decisiones-de-limpieza-not_drops.md"
]

labels_dict = {}

for file_path in md_files:
    if not os.path.exists(file_path):
        print("Missing:", file_path)
        continue
    
    count = 0
    desc_idx = 1 # default
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('|') and 'Variable' in line and 'Descripción' in line:
                headers = [c.strip().lower() for c in line.split('|')[1:-1]]
                for i, h in enumerate(headers):
                    if 'descripci' in h:
                        desc_idx = i
                        break
                continue
                
            if line.startswith('|') and not line.startswith('| :') and not line.startswith('| Variable'):
                cols = [c.strip() for c in line.split('|')[1:-1]]
                if len(cols) > desc_idx:
                    var_name = re.sub(r'[\*\`\s]', '', cols[0])
                    if var_name == "": continue
                    desc = cols[desc_idx].strip()
                    # Remove any markdown link or extra formatting in description if any
                    desc = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', desc)
                    
                    # Store both lowercase and uppercase to cover all bases just in case
                    label = f"{var_name} - {desc}"
                    labels_dict[var_name] = label
                    labels_dict[var_name.upper()] = label
                    labels_dict[var_name.lower()] = label
                    count += 1
    print(f"Read {count} variables from {os.path.basename(file_path)}")

with open("mnp/configs/column_labels.py", "w", encoding='utf-8') as f:
    f.write('"""Diccionario autogenerado para Sweetviz"""\n\n')
    f.write('SWEETVIZ_LABELS = ')
    f.write(json.dumps(labels_dict, indent=4, ensure_ascii=False))
    f.write('\n')

print(f"Generated {len(labels_dict)} unique label keys in total.")
