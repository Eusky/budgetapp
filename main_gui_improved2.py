# 변경점: global 변수 삭제(대신 lambda 함수로 인자 전달), 캘린더 위젯 생성 함수 추가
# 변경점: main() 함수 생성, tk 버튼 함수 인자 lambda 이용해서 전달하도록 수정, 년 단위 통계 보여주기 오동작 수정, set_date() 함수 버튼 이름 중복 수정
# 변경점: 캘린더 위젯 언어 설정(한국어)


import os
import tkinter as tk
import json
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime

# JSON 파일 경로를 실행 파일 기준으로 설정
def get_data_file_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "expenses.json")

# JSON 파일 읽기 및 생성
def create_file():
    data_file_path = get_data_file_path()
    if not os.path.exists(data_file_path):
        with open(data_file_path, "w", encoding="utf-8") as file:
            json.dump([], file, indent=4, ensure_ascii=False)

#  캘린더 위젯 생성 함수
def cal_make(right_frame, current_year, current_month, current_day):
    cal = Calendar(right_frame, locale="ko_KR", selectmode = 'day', year = current_year, month = current_month, day = current_day)
    return cal

# ========================================== GUI 버튼 함수 ==========================================

# 날짜를 설정하는 함수
def set_date(right_frame, current_year, current_month, current_day): 

    # 오른쪽 프레임의 내용 지우기
    for widget in right_frame.winfo_children():
        widget.destroy()
    
    # 새로운 내용 추가
    label = tk.Label(right_frame, text = "날짜를 선택하세요.")
    label.pack(pady = 10)

    # 미리 만든 캘린더 위젯 배치
    cal = cal_make(right_frame, current_year, current_month, current_day)
    cal.pack(pady = 10)

    # 날짜 저장 버튼 생성
    btn_save_for_record = tk.Button(right_frame, text = "해당 날짜 수입/지출 기록하기", command = lambda : record_income_and_expense(cal, right_frame)) 
    # 함수에 날짜를 전달하기 위해서 사용
    btn_save_for_record.pack(pady = 10)

    # 기록 조회 버튼 생성
    btn_save_for_show = tk.Button(right_frame, text = "해당 날짜 수입/지출 기록 조회하기", command = lambda : show_records(cal, right_frame)) 
    btn_save_for_show.pack(pady = 10)


# 수입/지출을 기록하는 함수
def record_income_and_expense(cal, right_frame): 

    # 캘린더에서 날짜 선택
    selected_date = cal.get_date()

    # 오른쪽 프레임의 내용 지우기
    for widget in right_frame.winfo_children():
        widget.destroy()
    
    # 선택된 날짜 표시
    label_selected_date = tk.Label(right_frame, text = f"날짜 : {selected_date}")
    label_selected_date.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = "w")  # sticky = "west": 왼쪽 정렬

    # 사용자 입력에 대한 안내문구 추가
    label_item = tk.Label(right_frame, text = "수입/지출 내용을 입력해주세요:")
    label_item.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = "w")  
    label_income = tk.Label(right_frame, text = "금액을 입력해주세요. 지출은 -를 붙여서 입력해주세요:")
    label_income.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = "w")  

    # 텍스트 입력을 받을 Entry 위젯 생성
    entry_item = tk.Entry(right_frame, width = 30)
    entry_item.grid(row = 1, column = 1, pady = 10)

    entry_income = tk.Entry(right_frame, width = 30)
    entry_income.grid(row = 2, column = 1, pady = 10)

    # 저장 버튼 생성
    btn_save = tk.Button(right_frame, text = "저장", command = lambda : save_to_json(entry_item, entry_income, cal)) # 엔트리 입력을 전달
    btn_save.grid(row = 3, column = 1, pady = 10)

# 데이터를 JSON 파일에 저장
def save_to_json(entry_item, entry_income, cal): 
    # 날짜 설정
    selected_date = cal.get_date()

    # 엔트리 입력을 읽어서 저장
    item = entry_item.get()
    income = int(entry_income.get())
    data = {
        "날짜": selected_date,
        "항목": item,
        "금액": income
    } 
    # JSON 파일에서 기존 데이터 읽기
    try:
        with open("expenses.json", "r", encoding = "utf-8") as file:
            expenses_data = json.load(file)
    # 파일이 비어 있을 경우 새 리스트 생성
    except json.JSONDecodeError:
        expenses_data = [] 

    # 데이터 추가
    expenses_data.append(data)
    
    # 다시 JSON 파일에 저장
    with open("expenses.json", "w", encoding = "utf-8") as file:
        json.dump(expenses_data, file, indent = 4, ensure_ascii = False) # indent = 4 : json 파일의 들여쓰기를 4칸으로 설정, ensure_ascii = False : 한글 작성이 가능하도록 설정
    
    # 엔트리 위젯의 입력 내용을 삭제
    entry_item.delete(0, tk.END)
    entry_income.delete(0, tk.END)
    
    # 저장이 완료되었음을 사용자에게 알림
    messagebox.showinfo("저장 완료", f"{item}: {income} 이 성공적으로 저장되었습니다.")

# 기록을 조회하는 함수
def show_records(cal, right_frame):
    selected_date = cal.get_date()

    # 오른쪽 프레임의 내용 지우기
    for widget in right_frame.winfo_children():
        widget.destroy()

    # JSON 파일에서 기존 데이터 읽기
    try:
        with open("expenses.json", "r", encoding = "utf-8") as file:
            expenses_data = json.load(file)

    # 파일이 비어 있을 경우 알림문구 출력
    except json.JSONDecodeError:
        messagebox.showerror("알림", "기록이 존재하지 않습니다.")

    # 데이터가 존재하는지 판단하기 위한 변수
    is_exist = False

    # 해당 날짜의 데이터 출력
    for data in expenses_data:
        if data["날짜"] == selected_date:
            label_result = tk.Label(right_frame, text = str(data)) 
            label_result.pack(pady = 10)
            is_exist = True 

    # 데이터가 존재하지 않을 경우 알림문구 출력
    if not is_exist:
        messagebox.showerror("알림", "기록이 존재하지 않습니다.")

# 통계를 보여주는 함수
def show_statistics(right_frame, current_year, current_month, current_day):

    # 오른쪽 프레임의 내용 지우기
    for widget in right_frame.winfo_children():
        widget.destroy()
    
    # 새로운 내용 추가
    label = tk.Label(right_frame, text = "통계 보여주기")
    label.pack(pady = 10)

    # 년월일 단위 버튼 생성
    day_button = tk.Button(right_frame, text = "일 단위 통계 보기", command = lambda : statistics_day(right_frame, current_year, current_month, current_day))
    day_button.pack(pady = 10)

    month_button = tk.Button(right_frame, text = "월 단위 통계 보기", command = lambda : statistics_month(right_frame, current_year, current_month))
    month_button.pack(pady = 10)

    year_button = tk.Button(right_frame, text = "년 단위 통계 보기", command = lambda : statistics_year(right_frame, current_year))
    year_button.pack(pady = 10)

# 일 단위 통계 보여주기
def statistics_day(right_frame, current_year, current_month, current_day):
    # 오른쪽 프레임의 내용 지우기
    for widget in right_frame.winfo_children():
        widget.destroy()

    # 날짜 선택 문구 
    label = tk.Label(right_frame, text = "날짜를 선택하세요.")
    label.pack(pady = 10)

    # Calendar 위젯 생성
    cal = cal_make(right_frame, current_year, current_month, current_day)
    cal.pack(pady = 10)

    # 날짜 저장 버튼 생성
    btn_save = tk.Button(right_frame, text = "해당 날짜 수입/지출 통계 보기", command = lambda : save_date_day(cal, right_frame))
    btn_save.pack(pady = 10)

def save_date_day(cal, right_frame):
    # 날짜에서 값 읽어와서 저장
    selected_date = cal.get_date()
    
    # JSON 파일에서 기존 데이터 읽기
    try:
        with open("expenses.json", "r", encoding = "utf-8") as file:
            expenses_data = json.load(file)

        # 총 수입/지출을 나타내는 변수
        total_income = 0
        total_expense = 0
        
        # 파일의 데이터를 불러오고 수입/지출 합산
        for data in expenses_data:
            if data["날짜"] == selected_date:
                if data["금액"] >= 0: 
                    total_income += data["금액"]
                else:
                    total_expense += data["금액"]

        # 총 수입/지출을 출력
        label = tk.Label(right_frame, text = f"총 수입: {total_income}, 총 지출: {total_expense} 입니다.")
        label.pack(pady = 10)

    # 파일이 비어 있을 경우 알림문구 출력
    except json.JSONDecodeError:
        messagebox.showerror("알림", "기록이 존재하지 않습니다.")

# 월 단위 통계 보여주기
def statistics_month(right_frame, current_year, current_month):

    # 오른쪽 프레임의 내용 지우기
    for widget in right_frame.winfo_children():
        widget.destroy()

    # 새로운 내용 추가
    label = tk.Label(right_frame, text = "월을 선택하세요.")
    label.pack(pady = 10)

    # 연도와 월 선택 리스트 생성
    years = [str(year) for year in range(current_year - 10, current_year + 11)]  # 과거 10년부터 미래 10년까지
    months = [f"{month:02d}" for month in range(1, 13)]  # "01" ~ "12"

    # 연도와 월 선택 콤보박스 생성
    year_combobox = ttk.Combobox(right_frame, values = years, state = "readonly", width = 10)
    year_combobox.set(str(current_year))  # 기본값 설정
    year_combobox.pack(pady = 10)

    month_combobox = ttk.Combobox(right_frame, values = months, state = "readonly", width = 10)
    month_combobox.set(str(current_month))  # 기본값 설정
    month_combobox.pack(pady = 10)

    # 선택된 값을 출력하는 버튼
    btn = tk.Button(right_frame, text = "월 선택", command = lambda : save_date_month(month_combobox, right_frame))
    btn.pack(pady = 10)

def save_date_month(month_combobox, right_frame):

    # JSON 파일에서 기존 데이터 읽기
    try:
        with open("expenses.json", "r", encoding = "utf-8") as file:
            expenses_data = json.load(file)

        month = month_combobox.get()

        total_income = 0
        total_expense = 0

        for data in expenses_data:
            # 24. 11. 16 형태의 날짜에서 4번째 인덱스부터 일치하는지 검사
            if str(data["날짜"]).startswith(month, 4):
                if data["금액"] >= 0:
                    total_income += data["금액"] 
                else:
                    total_expense += data["금액"]

        # 총 수입/지출을 출력
        label = tk.Label(right_frame, text = f"{month}월의 총 수입: {total_income}, 총 지출: {total_expense} 입니다.")
        label.pack(pady = 10)

    # 파일이 비어 있을 경우 알림문구 출력
    except json.JSONDecodeError:
        messagebox.showinfo("알림", "기록이 존재하지 않습니다.")

    

# 년 단위 통계 보여주기
def statistics_year(right_frame, current_year):

    # 오른쪽 프레임의 내용 지우기
    for widget in right_frame.winfo_children():
        widget.destroy()

    # 새로운 내용 추가
    label = tk.Label(right_frame, text = "연도를 선택하세요.")
    label.pack(pady = 10)

    # 연도 선택 리스트 생성
    years = [str(year) for year in range(current_year - 10, current_year + 11)]  # 과거 10년부터 미래 10년까지

    # 연도와 월 선택 콤보박스 생성
    year_combobox = ttk.Combobox(right_frame, values = years, state = "readonly", width = 10)
    year_combobox.set(str(current_year))  # 기본값 설정
    year_combobox.pack(pady = 10)

    # 선택된 값을 출력하는 버튼
    btn = tk.Button(right_frame, text = "연도 선택", command = lambda : save_date_year(year_combobox, right_frame))
    btn.pack(pady = 10)

def save_date_year(year_combobox, right_frame):
    # JSON 파일에서 기존 데이터 읽기
    try:
        with open("expenses.json", "r", encoding = "utf-8") as file:
            expenses_data = json.load(file)

        # 2024 형식으로 받아온 연도를 24 형식으로 변환
        year = year_combobox.get()
        simple_year = year[2:4] # 문자열 슬라이싱은 마지막은 포함 안되므로 2:4까지
        
        total_income = 0
        total_expense = 0

        for data in expenses_data:
            # 데이터가 선택된 연도로 시작하는지 검사
            if str(data["날짜"]).startswith(simple_year):
                if data["금액"] >= 0:
                    total_income += data["금액"] 
                else:
                    total_expense += data["금액"]

        # 총 수입/지출을 출력
        label = tk.Label(right_frame, text = f"{year}년의 총 수입: {total_income}, 총 지출: {total_expense} 입니다.")
        label.pack(pady = 10)

    # 파일이 비어 있을 경우 알림문구 출력
    except json.JSONDecodeError:
        messagebox.showinfo("알림", "기록이 존재하지 않습니다.")

# 프로그램 종료 함수
def close_program(root):
    root.destroy()

# ========================================== 메인 함수 ==========================================
def main():

    # 메인 윈도우 설정
    root = tk.Tk() # Tk 클래스로 새로운 창 생성 
    root.title("가계부 프로그램") 
    root.geometry("1024x576")

    # 왼쪽 프레임 (메뉴)
    left_frame = tk.Frame(root)
    left_frame.pack(side = "left")

    # 왼쪽 프레임에 메뉴 버튼 추가
    income_expense_button = tk.Button(left_frame, text = "수입/지출 기록하기", command = lambda : set_date(right_frame, current_year, current_month, current_day))
    income_expense_button.pack(padx = 10, pady = 10, fill = "x")

    statistics_button = tk.Button(left_frame, text = "통계 보여주기", command = lambda : show_statistics(right_frame, current_year, current_month, current_day))
    statistics_button.pack(padx = 10, pady = 10, fill = "x")

    exit_button = tk.Button(left_frame, text = "프로그램 종료", command = lambda : close_program(root))
    exit_button.pack(padx = 10, pady = 10, fill = "x")

    # 오른쪽 프레임 (내용 표시)
    right_frame = tk.Frame(root, bg = "white")
    right_frame.pack(side = "right", fill = "both", expand = True)

    # 현재 날짜 가져오기
    today = datetime.today()
    current_year = today.year # 2024 같은 형식으로 반환(정수형)
    current_month = today.month # 11 같은 형식으로 반환(정수형)
    current_day = today.day # 19 같은 형식으로 반환(정수형)

    # Tkinter 메인 루프 시작
    root.mainloop()

main()