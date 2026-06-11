import re
import json

nd_file = "notebooks/01_data_understanding/rech23_geografia/decisiones-de-limpieza-not-drops.md"
d_file = "notebooks/01_data_understanding/rech23_geografia/decisiones-de-limpieza.md"

def extract_rows(file_path):
    rows = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('| **'):
                cols = [c.strip() for c in line.split('|')[1:-1]]
                if len(cols) < 7: continue
                var_name = cols[0].replace('**', '').strip()
                tipo = cols[4]
                accion = cols[5]
                estado = cols[6]
                dict_year = cols[-2] if len(cols) > 9 else ""
                rows.append({
                    'var': var_name,
                    'accion': accion,
                    'estado': estado,
                    'dict_year': dict_year
                })
    return rows

nd_rows = extract_rows(nd_file)
d_rows = extract_rows(d_file)

drops = [r['var'] for r in d_rows if r['estado'] == 'DROP']

false_nums = {}
coalesce = {}
config_f3 = {}

for r in nd_rows:
    var = r['var']
    acc = r['accion']
    st = r['estado']
    dy = r['dict_year']

    # falsos numericos
    if "Reemplazar" in acc and "por NaN" in acc:
        match = re.search(r"Reemplazar (.*?) por NaN", acc)
        if match:
            nums_str = match.group(1).replace(" y ", ",")
            nums = []
            for n in nums_str.split(','):
                n = n.strip()
                if n:
                    try: nums.append(float(n))
                    except: pass
            if nums:
                false_nums[var] = nums

    # coalesce mapping basic attempt
    if st == 'COALESCE' and "COMBINAR con" in acc:
        match = re.search(r"COMBINAR con (.*)", acc)
        if match:
            targets_str = match.group(1)
            # Find words that look like SH... or HV...
            targets = re.findall(r"([A-Z]{2,3}\d+[A-Z_a-z0-9]*)", targets_str)
            if targets:
                for t in targets:
                    if t not in coalesce:
                        coalesce[t] = [t]
                    if var not in coalesce[t]:
                        coalesce[t].append(var)

    # config_f3
    if "20" in dy:
        m = re.search(r"20\d\d", dy)
        if m:
            config_f3[var] = int(m.group(0))

print("DROPS:", len(drops))
print("FALSE NUMS:", len(false_nums))
print("COALESCE:", len(coalesce))
print("F3:", len(config_f3))

with open("scratch/rech23_draft.py", "w") as f:
    f.write("from typing import Dict, Any\n\n")
    f.write("config_f1: Dict[str, Any] = {\n")
    f.write("    'keys_to_cast': ['HHID'],\n")
    f.write("    'false_numerics': " + json.dumps(false_nums, indent=4) + ",\n")
    f.write("    'cols_to_drop': " + json.dumps(drops, indent=4) + ",\n")
    f.write("    'coalesce': " + json.dumps(coalesce, indent=4) + ",\n")
    f.write("}\n\n")
    f.write("config_f3 = " + json.dumps(config_f3, indent=4) + "\n")
