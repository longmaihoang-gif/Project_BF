import os
import json
import re
import unicodedata

def remove_accents(input_str):
    if not input_str: return ""
    nks = unicodedata.normalize('NFKD', input_str)
    out = "".join([c for c in nks if not unicodedata.combining(c)])
    out = out.replace('đ', 'd').replace('Đ', 'D')
    out = re.sub(r'[^a-zA-Z0-9\s]', '', out)
    out = out.strip().replace(' ', '_')
    if out and out[0].isdigit(): out = "v_" + out
    return out

def process_god_mode_v2():
    root_dir = r"d:\Project_BF"
    settings_path = os.path.join(root_dir, "ProjectSettings", "EditorGenSymbolSetting.asset")
    enum_path = os.path.join(root_dir, "ProjectSettings", "ECAEnumSetting.asset")
    type_path = os.path.join(root_dir, "ProjectSettings", "ECATypeSetting.asset")
    
    if not os.path.exists(settings_path): return

    with open(settings_path, 'r', encoding='utf-8') as f:
        settings = json.loads(f.read().split('//"{FE:')[0].strip())

    # 1. ENUMS
    if os.path.exists(enum_path):
        with open(enum_path, 'r', encoding='utf-8') as f:
            enum_data = json.loads(f.read().split('//"{FE:')[0].strip())
        enums_target = settings.setdefault("GenSymbol", {}).setdefault("Enums", {})
        for ek, ev in enum_data.get("enumDefines", {}).items():
            e_entry = enums_target.setdefault(ek, {"label": remove_accents(ev.get("label")), "members": {}})
            for member in ev.get("info", []):
                m_key = member.get("key")
                if m_key: e_entry["members"][m_key] = {"label": remove_accents(member.get("label"))}

    # 2. COMPONENTS
    if os.path.exists(type_path):
        with open(type_path, 'r', encoding='utf-8') as f:
            type_data = json.loads(f.read().split('//"{FE:')[0].strip())
        comp_target = settings.setdefault("GenSymbol", {}).setdefault("Components", {})
        for tk, tv in type_data.get("TypeDefines", {}).items():
            if tk.startswith("CustomComponent"):
                c_entry = comp_target.setdefault(tk, {"label": remove_accents(tv.get("label")), "props": {}})
                for prop in tv.get("PropDefines", []):
                    p_id = str(prop.get("propID"))
                    c_entry["props"][p_id] = {"label": remove_accents(prop.get("label"))}

    # 3. GRAPHS (QUÉT CẢ FNA VÀ FNV)
    graphs = settings.setdefault("GenSymbol", {}).setdefault("Graphs", {})
    assets_dir = os.path.join(root_dir, "Assets")
    for root, dirs, files in os.walk(assets_dir):
        for file in files:
            if file.endswith(".eca"):
                eca_path = os.path.join(root, file)
                meta_path = eca_path + ".meta"
                if not os.path.exists(meta_path): continue
                with open(meta_path, 'r', encoding='utf-8') as f:
                    file_id = json.load(f).get("fileId")
                if not file_id: continue
                try:
                    with open(eca_path, 'r', encoding='utf-8') as f:
                        eca_data = json.loads(f.read().split('//"{FE:')[0].strip())
                except: continue

                g_entry = graphs.setdefault(file_id, {"label": remove_accents(file[:-4]) + "_ECA", "vars": {}, "funcs": {}})
                
                # Quét cả fna (Action) và fnv (Value Function)
                for block in eca_data.get("blocks", {}).get("blocks", []):
                    if block.get("type") in ["fna", "fnv"]:
                        fid = block.get("id")
                        fname = block.get("fields", {}).get("N") or block.get("extraState", {}).get("name")
                        if fid and fname:
                            f_item = g_entry["funcs"].setdefault(fid, {"label": remove_accents(fname)})
                            f_item.setdefault("params", {})
                            params = block.get("extraState", [])
                            if isinstance(params, list):
                                for p in params:
                                    pid, pname = p.get("id"), p.get("name")
                                    if pid and pname: f_item["params"][pid] = {"label": remove_accents(pname)}

                for var in eca_data.get("variables", []):
                    vid, vname = var.get("id"), var.get("name")
                    if vid and vname: g_entry["vars"][vid] = {"label": remove_accents(vname)}

    with open(settings_path, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)
    
    print("Pan-paka-pan! GOD MODE V2: Đã quét sạch fna, fnv và mọi ngóc ngách!")

if __name__ == "__main__":
    process_god_mode_v2()
