import os
import re
import random
import string
import shutil

def generate_random_id(length=8):
    """Tạo ID ngẫu nhiên cho _entityId"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def generate_file_id():
    """Tạo fileId ngẫu nhiên cho các tệp meta"""
    part1 = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(11))
    part2 = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
    part3 = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(11))
    return f"{part1}-{part2}-{part3}"

def main():
    base_dir = r"D:\Project_BF\Assets\General_BF_Assets\Characters"
    ref_mat_path = os.path.join(base_dir, "B_Aris", "EyeMouth_3D.mat")
    
    # Chuỗi mẫu trong B_Aris\EyeMouth_3D.mat cần thay thế
    ref_mat_tex_fileId = "k0zogzp41h-mkuholyv-1cy93jwakg5"
    ref_mat_tex_filePath = r"Assets\\Character\\B_Aris\\CH0334_EyeMouth.png"
    
    if not os.path.exists(base_dir):
        print(f"Không tìm thấy thư mục gốc: {base_dir}")
        return
    if not os.path.exists(ref_mat_path):
        print(f"Không tìm thấy tệp vật liệu mẫu: {ref_mat_path}")
        return

    for item in os.listdir(base_dir):
        char_dir = os.path.join(base_dir, item)
        
        if not os.path.isdir(char_dir):
            continue
            
        # Bỏ qua thư mục Aris và B_Aris
        if item == "Aris" or item == "B_Aris":
            continue
            
        print(f"\nĐang xử lý thư mục: {item}")
        
        # 1. Tìm base ID từ tệp .prefab gốc
        base_prefab = None
        base_id = ""
        
        # Danh sách các từ khóa cần loại trừ trong tên file (không phân biệt chữ hoa/thường)
        exclude_keywords = ["_3d", "mouth", "shield", "_ex", "_vfx", "core", "bullet", "missile", "drone", "turret", "trap", "effect"]
        
        for f in os.listdir(char_dir):
            if f.endswith(".prefab"):
                f_lower = f.lower()
                # Kiểm tra xem tên file có chứa bất kỳ từ khóa loại trừ nào không
                is_valid = True
                for kw in exclude_keywords:
                    if kw in f_lower:
                        is_valid = False
                        break
                        
                if is_valid:
                    base_prefab = f
                    base_id = f.replace(".prefab", "")
                    # Ưu tiên các file có chứa từ khóa 'original' hoặc khớp chính xác chuẩn CHxxxx
                    if "original" in f_lower or re.match(r"^CH\d+(_\d+)?\.prefab$", f, re.IGNORECASE):
                        break # Đã tìm thấy ứng viên hoàn hảo nhất, thoát vòng lặp
        
        if not base_prefab:
            print(f"  -> Không tìm thấy prefab gốc, bỏ qua.")
            continue
            
        print(f"  -> Tìm thấy Base ID: {base_id}")
        
        # Tìm ảnh EyeMouth của nhân vật hiện tại để lấy fileId
        eye_mouth_img = f"{base_id}_EyeMouth.png"
        eye_mouth_img_path = os.path.join(char_dir, eye_mouth_img)
        eye_mouth_img_meta = eye_mouth_img_path + ".meta"
        
        target_tex_fileId = ""
        if os.path.exists(eye_mouth_img_meta):
            with open(eye_mouth_img_meta, 'r', encoding='utf-8') as mf:
                match = re.search(r'"fileId":\s*"([^"]+)"', mf.read())
                if match:
                    target_tex_fileId = match.group(1)
        
        # 2. Xử lý EyeMouth_3D.mat (Copy từ B_Aris sang)
        mat_3d_path = os.path.join(char_dir, "EyeMouth_3D.mat")
        new_mat_file_id = generate_file_id()
        
        shutil.copy2(ref_mat_path, mat_3d_path)
        
        # Cập nhật đường dẫn và fileId của ảnh EyeMouth bên trong vật liệu
        with open(mat_3d_path, 'r', encoding='utf-8') as f:
            mat_content = f.read()
            
        if target_tex_fileId:
            mat_content = mat_content.replace(ref_mat_tex_fileId, target_tex_fileId)
            
        # Đường dẫn mới cho thuộc tính filePath của Texture
        target_tex_filePath_json = f"Assets\\\\General_BF_Assets\\\\Characters\\\\{item}\\\\{eye_mouth_img}"
        mat_content = mat_content.replace(ref_mat_tex_filePath, target_tex_filePath_json)
        
        with open(mat_3d_path, 'w', encoding='utf-8') as f:
            f.write(mat_content)
            
        # Tạo file meta cho EyeMouth_3D.mat
        meta_3d_path = mat_3d_path + ".meta"
        with open(meta_3d_path, 'w', encoding='utf-8') as mf:
            mf.write(f'{{\n  "fileId": "{new_mat_file_id}"\n}}')
            
        print(f"  -> Đã tạo EyeMouth_3D.mat từ mẫu B_Aris")
        
        # Trích xuất fileId của EyeMouth.mat cũ để thay vào prefab 3D
        old_mat_file_id = ""
        old_mat_meta_path = os.path.join(char_dir, "EyeMouth.mat.meta")
        if os.path.exists(old_mat_meta_path):
            with open(old_mat_meta_path, 'r', encoding='utf-8') as mf:
                match = re.search(r'"fileId":\s*"([^"]+)"', mf.read())
                if match:
                    old_mat_file_id = match.group(1)
                    
        # 3. Xử lý .prefab
        prefab_path = os.path.join(char_dir, base_prefab)
        prefab_3d_path = os.path.join(char_dir, f"{base_id}_3D.prefab")
        new_prefab_file_id = generate_file_id()
        
        if os.path.exists(prefab_path):
            with open(prefab_path, 'r', encoding='utf-8') as pf:
                prefab_content = pf.read()
            
            # Sửa scale thành 85, 85, 85
            prefab_content = re.sub(
                r'"scale":\s*\{\s*"x":\s*[0-9.]+,\s*"y":\s*[0-9.]+,\s*"z":\s*[0-9.]+\s*\}',
                '"scale": {\n        "x": 85,\n        "y": 85,\n        "z": 85\n      }',
                prefab_content,
                count=1 # Chỉ sửa khối UGCSceneEntity gốc
            )
            
            # Thay ID vật liệu cũ EyeMouth thành ID mới của EyeMouth_3D
            if old_mat_file_id:
                prefab_content = prefab_content.replace(old_mat_file_id, new_mat_file_id)
                prefab_content = prefab_content.replace("EyeMouth.mat", "EyeMouth_3D.mat")
                
            # Gắn AnimatorController .ac vào prefab
            ac_path_escaped = f"Assets\\\\General_BF_Assets\\\\Characters\\\\{item}\\\\{base_id}.ac"
            ac_ref_str = f'''"AnimationControllerAble": {{
          "acRef": {{
            "fileId": "{generate_file_id()}",
            "filePath": "{ac_path_escaped}",
            "_tag": {{
              "type": "GFileRefer"
            }},
            "fileType": "ac"
          }}
        }}'''
            
            if '"AnimationControllerAble": {}' in prefab_content:
                prefab_content = prefab_content.replace('"AnimationControllerAble": {}', ac_ref_str)
            
            with open(prefab_3d_path, 'w', encoding='utf-8') as pf:
                pf.write(prefab_content)
                
            # Copy/Tạo file meta cho prefab 3D
            meta_path = prefab_path + ".meta"
            meta_3d_path = prefab_3d_path + ".meta"
            if os.path.exists(meta_path):
                with open(meta_path, 'r', encoding='utf-8') as mf:
                    meta_content = mf.read()
                    match = re.search(r'"fileId":\s*"([^"]+)"', meta_content)
                    if match:
                        new_meta_content = meta_content.replace(match.group(1), new_prefab_file_id)
                        with open(meta_3d_path, 'w', encoding='utf-8') as mf:
                            mf.write(new_meta_content)
            print(f"  -> Đã tạo {base_id}_3D.prefab")

    print("\nHoàn tất xử lý kịch bản phiên bản 2!")

if __name__ == "__main__":
    main()
