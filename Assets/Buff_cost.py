import csv
import os

# Đường dẫn đến "Kho báu" dữ liệu
file_path = r'd:\Project_BF\Assets\Localization\Thuộc tính 1.csv'

# Chỉ số Buff (Level Max!)
NEW_COST_RECOVERY = "3000"
NEW_MAX_COST = "20"

def buff_students():
    print(f"🎮 Aris đang khởi động tiến trình Patch: {file_path}")
    
    if not os.path.exists(file_path):
        print("❌ Lỗi: Không tìm thấy file dữ liệu! Quest fail!")
        return

    try:
        with open(file_path, mode='r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            fieldnames = reader.fieldnames
            
            # Kiểm tra xem các thuộc tính cần thiết có tồn tại không
            required_fields = ['Cost_Recovery', 'Max_Cost']
            for field in required_fields:
                if field not in fieldnames:
                    print(f"❌ Lỗi: Thuộc tính '{field}' không tồn tại trong file!")
                    return

            rows = []
            count = 0
            for row in reader:
                # Buff cho tất cả các thực thể (trừ dòng empty nếu cần)
                if row['ID'] != 'empty':
                    row['Cost_Recovery'] = NEW_COST_RECOVERY
                    row['Max_Cost'] = NEW_MAX_COST
                    count += 1
                rows.append(row)

        # Ghi đè lại file với chỉ số mới
        with open(file_path, mode='w', encoding='utf-8', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
            
        print(f"✅ Pan-paka-pan! Đã Buff thành công cho {count} học sinh!")
        print(f"🚀 Chỉ số hiện tại -> Cost Recovery: {NEW_COST_RECOVERY} | Max Cost: {NEW_MAX_COST}")

    except Exception as e:
        print(f"⚠️ Đã xảy ra lỗi trong quá trình thực thi Quest: {e}")

if __name__ == "__main__":
    buff_students()
