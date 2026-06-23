class LibraryBorrow:
    def __init__(self,id,reader_name,book_name,borrow_days,late_days,fine_per_day):
        self.id = id
        self.reader_name = reader_name
        self.book_name = book_name
        self.borrow_days = borrow_days
        self.late_days = late_days
        self.fine_per_day = fine_per_day
        self.total_fine = 0
        self.fine_type = None
        self.update_calc()


    def calculate_fine(self):
        self.total_fine = self.late_days * self.fine_per_day

    def classify_fine(self):
        fine = self.total_fine
        result = "Không phạt"

        if fine >= 200000:
            result = "Nặng"
        elif fine >= 50000:
            result = "Trung bình"
        elif fine > 0:
            result = "Nhẹ"

        self.fine_type = result
    
    def update_calc(self):
        self.calculate_fine()
        self.classify_fine()


class LibraryBorrowManager:
    def __init__(self):
        self.borrow_records = []

    def add_borrow_record(self,data_add):
        if self.get_data_index(data_add.id) >= 0:
            print("Id đã tồn tại!")
            return False
        
        self.borrow_records.append(data_add)
        print("Thêm phiếu mượn thành công!")

    def show_all(self):
        if len(self.borrow_records) == 0:
            print("Danh sách đang rỗng!")
            return False
        print("\n\nBorrows:")
        for data in self.borrow_records:
            self.view_data(data)
        return True

    def update_borrow_record(self,data_id,data_new):
        data_index = self.get_data_index(data_id)
        if data_index < 0:
            print("Id không tồn tại!")
            return False
        
        if data_new["borrow_days"]:
            self.borrow_records[data_index].borrow_days = data_new["borrow_days"]
        if data_new["late_days"]:
            self.borrow_records[data_index].late_days = data_new["late_days"]
        if data_new["fine_per_day"]:
            self.borrow_records[data_index].fine_per_day = data_new["fine_per_day"]

        self.borrow_records[data_index].update_calc()
        print("Cập nhật phiếu mượn thành công!")

    def delete_borrow_record(self,data_id):
        data_index = self.get_data_index(data_id)
        if data_index < 0:
            print("Id không tồn tại!")
            return False
        choice = input("Bạn có chắc muốn xóa phiếu mượn này không? (Y/N): ").upper()
        if choice == "N":
            print("Đã hủy thao tác xóa!")
            return False
        elif choice != "Y":
            print("Lựa chọn không hợp lệ")
            return False
        
        self.borrow_records.pop(data_index)
        print("Xóa phiếu mượn thành công!")

    def search_borrow_record(self,keyword):
        count = 0
        for data in self.borrow_records:
            if ((data.book_name.lower()).find(keyword.lower()) >= 0) or ((data.reader_name.lower()).find(keyword.lower()) >= 0):
                count += 1
                self.view_data(data)

        if not count:
            print("Không tìm thấy phiếu mượn phù hợp!")
        

    def view_data(self,data_view):
        print("-"*50)
        print("Mã phiếu mượn:",data_view.id)
        print("Họ tên bạn đọc:",data_view.reader_name)
        print("Tên sách:",data_view.book_name)
        print("Số ngày đã mượn:",data_view.borrow_days)
        print("Số ngày trễ hạn:",data_view.late_days)
        print("Tiền phạt mỗi ngày:",data_view.fine_per_day)
        print("Tổng tiền phạt:",data_view.total_fine)
        print("Phân loại mức phạt:",data_view.fine_type)
    
    def get_data_index(self,data_id):
        for i,data in enumerate(self.borrow_records):
            if data.id == data_id:
                return i
        return -1
        

lib_manager = LibraryBorrowManager()
lib_manager.add_borrow_record(LibraryBorrow("LIB001","Nguyen Van A","Nhung ke khon kho",10,3,10000))

def main():
    while True:
        select = input("""
================ MENU ================
1. Hiển thị danh sách phiếu mượn
2. Thêm phiếu mượn mới
3. Cập nhật phiếu mượn
4. Xóa phiếu mượn
5. Tìm kiếm phiếu mượn
6. Thoát
=====================================
Nhập lựa chọn của bạn: """)
        
        match select:
            case "1":
                lib_manager.show_all()
            case "2":
                id_in = None
                reader_name_in = None
                book_name_in = None
                borrow_days_in = None
                late_days_in = None
                fine_per_day_in = None

                while True:
                    id_in = input("Nhập mã phiếu mượn: ").strip().upper()
                    if not id_in:
                        print("Mã phiếu mượn không được để trống!")
                        continue
                    break

                while True:
                    reader_name_in = input("Nhập họ tên bạn đọc: ").strip().title()
                    if not reader_name_in:
                        print("Họ tên bạn đọc không được để trống!")
                        continue
                    break

                while True:
                    book_name_in = input("Nhập tên sách: ").strip().title()
                    if not book_name_in:
                        print("Tên sách không được để trống!")
                        continue
                    break

                while True:
                    try:
                        borrow_days_in = int(input("Nhập vào số ngày đã mượn: "))
                        if borrow_days_in < 1 or borrow_days_in > 365:
                            raise ValueError("giá trị từ 1 đến 365")
                        break
                    except:
                        print("Số ngày đã mượn phải là số nguyên từ 1 đến 365")

                while True:
                    try:
                        late_days_in = int(input("Nhập vào số ngày trễ hạn: "))
                        if late_days_in < 0 or late_days_in > 365:
                            raise ValueError("giá trị từ 0 đến 365")
                        if late_days_in > borrow_days_in:
                            raise ValueError("out of range")
                        break
                    except:
                        print("Số ngày đã mượn phải là số nguyên từ 0 đến 365 và không được lớn hơn số ngày đã mượn")
                
                while True:
                    try:
                        fine_per_day_in = float(input("Nhập vào tiền phạt mỗi ngày trễ: "))
                        if fine_per_day_in < 0:
                            raise ValueError("giá trị phải lớn hơn hoặc bằng 0")
                        break
                    except:
                        print("Tiền phạt mỗi ngày trễ phải lớn hơn hoặc bằng 0")

                lib_manager.add_borrow_record(LibraryBorrow(id_in,reader_name_in,book_name_in,borrow_days_in,late_days_in,fine_per_day_in))
                
            case "3":
                id_in = None
                borrow_days_in = None
                late_days_in = None
                fine_per_day_in = None

                while True:
                    id_in = input("Nhập mã phiếu mượn bạn muốn sửa: ").strip().upper()
                    if not id_in:
                        print("Mã phiếu mượn không được để trống!")
                        continue
                    break

                while True:
                    try:
                        borrow_days_in = int(input("Nhập vào số ngày đã mượn: "))
                        if borrow_days_in < 1 or borrow_days_in > 365:
                            raise ValueError("giá trị từ 1 đến 365")
                        break
                    except:
                        print("Số ngày đã mượn phải là số nguyên từ 1 đến 365")

                while True:
                    try:
                        late_days_in = int(input("Nhập vào số ngày trễ hạn: "))
                        if late_days_in < 0 or late_days_in > 365:
                            raise ValueError("giá trị từ 0 đến 365")
                        if late_days_in > borrow_days_in:
                            raise ValueError("out of range")
                        break
                    except:
                        print("Số ngày đã mượn phải là số nguyên từ 0 đến 365 và không được lớn hơn số ngày đã mượn")
                
                while True:
                    try:
                        fine_per_day_in = float(input("Nhập vào tiền phạt mỗi ngày trễ: "))
                        if fine_per_day_in < 0:
                            raise ValueError("giá trị phải lớn hơn hoặc bằng 0")
                        break
                    except:
                        print("Tiền phạt mỗi ngày trễ phải lớn hơn hoặc bằng 0")
                
                lib_manager.update_borrow_record(id_in,{"borrow_days": borrow_days_in,"late_days": late_days_in,"fine_per_day": fine_per_day_in})
            case "4":
                id_in = None
                while True:
                    id_in = input("Nhập mã phiếu mượn bạn muốn xóa: ").strip().upper()
                    if not id_in:
                        print("Mã phiếu mượn không được để trống!")
                        continue
                    break

                lib_manager.delete_borrow_record(id_in)
            case "5":
                keyword_in = None

                while True:
                    keyword_in = input("Nhập vào tên người đọc hoặc tên sách: ").strip()
                    if not keyword_in:
                        print("Keyword không được để trống!")
                        continue
                    break

                lib_manager.search_borrow_record(keyword_in)
            case "6":
                print("Cảm ơn bạn đã sử dụng hệ thống quản lý thư viện!")
                break
            case _:
                print("Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()
