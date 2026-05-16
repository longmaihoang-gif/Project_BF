import re

# === TỪ ĐIỂN MẬT MÃ BẬC SSS (Hardcoded 100%) ===
# Aris đã trích xuất từ đống mật mã trong thư viện của Sensei
DECODE_TABLE = {
    "6": "_",          # Khoảng trắng
    "DT": "D",         # Đ
    "A9": "o",         # ọ (đã bỏ dấu)
    "Jc": "c",         # c (cuối từ)
    "ch": "ch",        
    "A9F": "i",        # ỉ (đã bỏ dấu)
    "s": "s",
    "A9N": "o",        # ố (đã bỏ dấu)
    "nh": "nh",
    "Cen": "an",       # ân (đã bỏ dấu)
    "v": "v",
    "A8it": "at",      # ật (đã bỏ dấu)
    "B": "B",
    "t": "t",
    "A8kt": "at",      # ắt (đã bỏ dấu)
    "n": "n",
    "C8": "u",         # ú (đã bỏ dấu)
    "th": "th",
    "Cw": "o",         # ô (đã bỏ dấu)
    "ng": "ng",
    "Fv": "u",         # ư (đã bỏ dấu)
    "A9Zn": "o",       # ờ (đã bỏ dấu)
    "Chuy": "Chuy",
    "A90": "e",        # ển (đã bỏ dấu)
    "Ti": "i",         # ỗi (đã bỏ dấu)
    "Cc": "a",         # ành (đã bỏ dấu)
    "A8_nh": "anh",    # ảnh
    "Bi": "Bi",
    "A8_m": "am",      # cảm
    "L": "L",          # L
    "ay": "ay",        # ấy
    "xA": "xu",        # xử
    "j": "ly",         # lý (đã mã hóa)
    "gi": "gi",
    "Cd": "a",         # trị (đã mã hóa)
    "tr": "tr",
    "H": "H",
    "ip": "ap",        # nhập
}

def decode_aris_logic(obfuscated_str):
    # Loại bỏ tiền tố và hậu tố __
    clean_str = obfuscated_str.strip("_")
    
    # Aris dùng thuật toán "Tham lam" (Greedy Match) để tìm từ dài nhất trước
    decoded = ""
    i = 0
    # Sắp xếp các key theo độ dài giảm dần để ưu tiên các mã dài (như A8_nh)
    sorted_keys = sorted(DECODE_TABLE.keys(), key=len, reverse=True)
    
    while i < len(clean_str):
        matched = False
        for key in sorted_keys:
            if clean_str.startswith(key, i):
                decoded += DECODE_TABLE[key]
                i += len(key)
                matched = True
                break
        if not matched:
            # Nếu không có trong từ điển, giữ nguyên ký tự đó
            decoded += clean_str[i]
            i += 1
            
    # Chuyển thành Snake Case đẹp đẽ
    return decoded.replace("__", "_").strip("_")

def main():
    print("=== ARIS STANDALONE DECODER V1.0 (OFFLINE 100%) ===")
    print("Dán mã __ABC__ vào để giải mã sang Tiếng Việt không dấu.")
    
    while True:
        user_input = input("\nNhập mã (exit để thoát): ").strip()
        if user_input.lower() == 'exit': break
        
        result = decode_aris_logic(user_input)
        print(f">> KẾT QUẢ: {result}")

if __name__ == "__main__":
    main()
