import re
import json
import unicodedata

def remove_accents(input_str):
    if not input_str: return ""
    nks = unicodedata.normalize('NFKD', input_str)
    out = "".join([c for c in nks if not unicodedata.combining(c)])
    out = out.replace('đ', 'd').replace('Đ', 'D')
    out = re.sub(r'[^a-zA-Z0-9]', '_', out)
    out = re.sub(r'_+', '_', out)
    return out.strip('_')

lib_path = r"d:\Project_BF\Temp\UGCLanguage\editorGen\EditorGenLib.fcc"
db = {}

with open(lib_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    
for i in range(len(lines)):
    line = lines[i].strip()
    if line.startswith("//"):
        original_name = line.replace("//", "").split('(')[0].strip()
        if i + 1 < len(lines):
            next_line = lines[i+1]
            match = re.search(r'(__\w+__)', next_line)
            if match:
                obf_name = match.group(1)
                db[obf_name] = remove_accents(original_name)

print("--- START DICTIONARY ---")
print(json.dumps(db, indent=4))
print("--- END DICTIONARY ---")
