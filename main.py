import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta

plt.rcParams['font.family'] = 'Malgun Gothic'

class StepBackApp:
    import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta

plt.rcParams['font.family'] = 'Malgun Gothic'

class StepBackApp:
    def __init__(self, master):
        self.master = master
        self.master.title("StepBack")
        self.master.geometry("800x600")
        self.master.configure(bg='#1E1E1E')

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#1E1E1E')
        self.style.configure('TButton', background='#3C3F41', foreground='white', font=('Malgun Gothic', 11))
        self.style.map('TButton', background=[('active', '#4C5052')])
        self.style.configure('TLabel', background='#1E1E1E', foreground='#CCCCCC', font=('Malgun Gothic', 11))
        self.style.configure('TCheckbutton', background='#1E1E1E', foreground='#CCCCCC', font=('Malgun Gothic', 11))
        self.style.configure('TLabelframe', background='#1E1E1E')
        self.style.configure('TLabelframe.Label', background='#1E1E1E', foreground='#CCCCCC', font=('Malgun Gothic', 12, 'bold'))

        self.activity_log = []
        self.progress_data = []
        self.goals = []
        self.load_data()
        self.goals = self.ensure_date_in_goals(self.goals)

        self.create_main_menu()

    def ensure_date_in_goals(self, goals):
        for goal in goals:
            if 'date' not in goal:
                goal['date'] = datetime.now().strftime("%Y-%m-%d")
        return goals

    def create_main_menu(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        # 메인 프레임 생성
        main_frame = ttk.Frame(self.master, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 앱 제목
        ttk.Label(main_frame, text="StepBack", font=("Malgun Gothic", 24, "bold"), 
                foreground="#4A90E2").pack(pady=(0, 20))

        # 콘텐츠를 담을 프레임
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # 스크롤 가능한 캔버스 생성
        canvas = tk.Canvas(content_frame, bg='#1E1E1E', highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Canvas.TFrame')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # 좌우 프레임 생성
        left_frame = ttk.Frame(scrollable_frame, padding=(0, 0, 20, 0))
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        right_frame = ttk.Frame(scrollable_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 왼쪽 메뉴 버튼
        ttk.Button(left_frame, text="불안도 체크", command=self.check_anxiety, width=20).pack(pady=5)
        ttk.Button(left_frame, text="기록 보기", command=self.view_records, width=20).pack(pady=5)

        # 목표 섹션
        goals_frame = ttk.LabelFrame(right_frame, text="오늘의 목표", padding=15)
        goals_frame.pack(fill=tk.X, pady=(0, 15))

        # 목표 입력 프레임
        goal_input_frame = ttk.Frame(goals_frame)
        goal_input_frame.pack(fill=tk.X, pady=(0, 10))

        goal_entry = tk.Text(goal_input_frame, width=40, height=1, 
                            font=('Malgun Gothic', 11), bg='#2B2B2B', fg='#CCCCCC',
                            insertbackground='#CCCCCC', padx=5, pady=3)
        goal_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(goal_input_frame, text="추가", 
                command=lambda: self.add_goal(goal_entry)).pack(side=tk.RIGHT)

        for i, goal in enumerate(self.goals):
            if goal.get('date', datetime.now().strftime("%Y-%m-%d")) == datetime.now().strftime("%Y-%m-%d"):
                self.create_goal_widget(goals_frame, i, goal)

        # 활동 섹션
        activities_frame = ttk.LabelFrame(right_frame, text="오늘의 활동", padding=15)
        activities_frame.pack(fill=tk.X)

        activity_input_frame = ttk.Frame(activities_frame)
        activity_input_frame.pack(fill=tk.X, pady=(0, 10))

        activity_entry = tk.Text(activity_input_frame, width=40, height=1, 
                            font=('Malgun Gothic', 11), bg='#2B2B2B', fg='#CCCCCC',
                            insertbackground='#CCCCCC', padx=5, pady=3)
        activity_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(activity_input_frame, text="추가", 
                command=lambda: self.add_activity(activity_entry)).pack(side=tk.RIGHT)

        for i, activity in enumerate(self.activity_log):
            if activity['date'].split()[0] == datetime.now().strftime("%Y-%m-%d"):
                self.create_activity_widget(activities_frame, i, activity)

        # 스크롤바와 캔버스 배치
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)




    def create_goal_widget(self, parent, index, goal):
        goal_frame = ttk.Frame(parent)
        goal_frame.pack(fill=tk.X, pady=5)
        
        var = tk.BooleanVar(value=goal['completed'])
        cb = ttk.Checkbutton(goal_frame, variable=var, command=lambda i=index, v=var: self.toggle_goal(i, v))
        cb.pack(side=tk.LEFT)
        
        if goal['completed']:
            goal_text = f"\u0336{goal['text']}\u0336"
        else:
            goal_text = goal['text']
        
        ttk.Label(goal_frame, text=goal_text, wraplength=300).pack(side=tk.LEFT, padx=(5, 10), fill=tk.X, expand=True)
        ttk.Button(goal_frame, text="삭제", width=5, command=lambda i=index: self.delete_goal(i)).pack(side=tk.RIGHT)

    def create_activity_widget(self, parent, index, activity):
        activity_frame = ttk.Frame(parent)
        activity_frame.pack(fill=tk.X, pady=5)
        ttk.Label(activity_frame, text=activity['activity'], wraplength=300).pack(side=tk.LEFT, padx=(5, 10), fill=tk.X, expand=True)
        ttk.Button(activity_frame, text="삭제", width=5, command=lambda i=index: self.delete_activity(i)).pack(side=tk.RIGHT)

    def add_goal(self, entry):
        goal = entry.get("1.0", tk.END).strip()
        if goal:
            self.goals.append({"date": datetime.now().strftime("%Y-%m-%d"), "text": goal, "completed": False})
            self.save_data()
            entry.delete("1.0", tk.END)
            self.create_main_menu()

    def add_activity(self, entry):
        activity = entry.get("1.0", tk.END).strip()
        if activity:
            self.activity_log.append({"date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "activity": activity})
            self.save_data()
            entry.delete("1.0", tk.END)
            self.create_main_menu()

    def check_anxiety(self):
        anxiety_window = tk.Toplevel(self.master)
        anxiety_window.title("불안도 체크")
        anxiety_window.geometry("300x200")
        anxiety_window.configure(bg='#1E1E1E')

        ttk.Label(anxiety_window, text="오늘의 불안 수준", font=("Malgun Gothic", 14)).pack(pady=10)

        self.anxiety_slider = ttk.Scale(
            anxiety_window, from_=1, to=10, orient=tk.HORIZONTAL, length=200,
            command=self.update_anxiety_label
        )
        self.anxiety_slider.set(5)
        self.anxiety_slider.pack(pady=10)

        self.anxiety_label = ttk.Label(anxiety_window, text="현재 불안 수준: 5", font=("Malgun Gothic", 12))
        self.anxiety_label.pack(pady=5)

        ttk.Button(anxiety_window, text="저장", command=lambda: self.save_anxiety(anxiety_window)).pack(pady=10)

    def update_anxiety_label(self, value):
        self.anxiety_label.config(text=f"현재 불안 수준: {int(float(value))}")

    def save_anxiety(self, window):
        anxiety_level = int(self.anxiety_slider.get())
        self.progress_data.append({"date": datetime.now().strftime("%Y-%m-%d"), "score": anxiety_level})
        self.save_data()
        messagebox.showinfo("저장 완료", f"오늘의 불안 수준 {anxiety_level}이 저장되었습니다.")
        window.destroy()
        self.create_main_menu()

    def toggle_goal(self, index, var):
        self.goals[index]['completed'] = var.get()
        self.save_data()
        self.create_main_menu()

    def delete_goal(self, index):
        del self.goals[index]
        self.save_data()
        self.create_main_menu()

    def delete_activity(self, index):
        del self.activity_log[index]
        self.save_data()
        self.create_main_menu()

    def view_records(self):
        records_window = tk.Toplevel(self.master)
        records_window.title("기록 보기")
        records_window.geometry("800x600")
        records_window.configure(bg='#1E1E1E')

        main_frame = ttk.Frame(records_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        records_canvas = tk.Canvas(main_frame, bg='#1E1E1E', highlightthickness=0)
        records_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=records_canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        records_canvas.configure(yscrollcommand=scrollbar.set)
        records_canvas.bind('<Configure>', lambda e: records_canvas.configure(scrollregion=records_canvas.bbox("all")))

        records_frame = ttk.Frame(records_canvas)
        records_canvas.create_window((0, 0), window=records_frame, anchor="nw")

        dates = sorted(set([goal['date'] for goal in self.goals] + 
                        [activity['date'].split()[0] for activity in self.activity_log] + 
                        [data['date'] for data in self.progress_data]), reverse=True)

        # 불안도 그래프
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(10, 4))
        fig.patch.set_facecolor('#1E1E1E')
        ax.set_facecolor('#1E1E1E')
        
        # 그리드 스타일 설정
        ax.grid(True, color='#333333', linestyle='--', alpha=0.3)
        
        # 테두리 색상 설정
        ax.spines['bottom'].set_color('#333333')
        ax.spines['top'].set_color('#333333')
        ax.spines['left'].set_color('#333333')
        ax.spines['right'].set_color('#333333')
        
        # 데이터 플롯
        ax.plot([datetime.strptime(date, "%Y-%m-%d") for date in dates], 
                [next((data['score'] for data in self.progress_data if data['date'] == date), None) for date in dates],
                marker='o', linestyle='-', color='#4A90E2', linewidth=2, 
                markersize=8, markerfacecolor='#4A90E2', markeredgecolor='white')
        
        # 레이블 설정
        ax.set_title("불안도 변화", fontsize=14, color='#CCCCCC', pad=20)
        ax.set_xlabel("날짜", fontsize=12, color='#CCCCCC', labelpad=10)
        ax.set_ylabel("불안도", fontsize=12, color='#CCCCCC', labelpad=10)
        
        # 눈금 설정
        ax.tick_params(colors='#CCCCCC', which='both')
        ax.set_ylim(0, 10)
        plt.xticks(rotation=45)
        
        # 여백 조정
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=records_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=(0, 20))

        for date in dates:
            date_frame = ttk.LabelFrame(records_frame, text=date, padding=10)
            date_frame.pack(fill=tk.X, pady=(0, 20))

            # 목표
            goals = [goal for goal in self.goals if goal['date'] == date]
            if goals:
                ttk.Label(date_frame, text="목표:", font=("Malgun Gothic", 10, "bold")).pack(anchor=tk.W)
                for goal in goals:
                    goal_text = f"{'[완료] ' if goal['completed'] else ''}{goal['text']}"
                    ttk.Label(date_frame, text=goal_text, wraplength=700).pack(anchor=tk.W, padx=(10, 0))

            # 활동
            activities = [activity for activity in self.activity_log if activity['date'].split()[0] == date]
            if activities:
                ttk.Label(date_frame, text="활동:", font=("Malgun Gothic", 10, "bold")).pack(anchor=tk.W, pady=(10, 0))
                for activity in activities:
                    ttk.Label(date_frame, text=activity['activity'], wraplength=700).pack(anchor=tk.W, padx=(10, 0))


    def save_data(self):
        data = {
            "activity_log": self.activity_log,
            "progress_data": self.progress_data,
            "goals": self.goals
        }
        with open("stepback_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

    def load_data(self):
        try:
            with open("stepback_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.activity_log = data.get("activity_log", [])
                self.progress_data = data.get("progress_data", [])
                self.goals = data.get("goals", [])
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = StepBackApp(root)
    root.mainloop()


    def ensure_date_in_goals(self, goals):
        for goal in goals:
            if 'date' not in goal:
                goal['date'] = datetime.now().strftime("%Y-%m-%d")
        return goals

    def create_main_menu(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        # 메인 캔버스와 스크롤바 생성
        main_canvas = tk.Canvas(self.master, bg='#1E1E1E', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.master, orient="vertical", command=main_canvas.yview)
        main_canvas.configure(yscrollcommand=scrollbar.set)

        # 스크롤바와 캔버스 배치
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 메인 프레임 생성
        main_frame = ttk.Frame(main_canvas, padding=20)
        main_canvas.create_window((0, 0), window=main_frame, anchor="nw", width=main_canvas.winfo_width())

        # 캔버스 크기 조정 시 이벤트 처리
        def configure_scroll_region(event):
            main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        
        def configure_window_size(event):
            main_canvas.itemconfig(main_canvas.find_withtag("win"), width=event.width)

        main_frame.bind("<Configure>", configure_scroll_region)
        main_canvas.bind("<Configure>", configure_window_size)

        # 앱 제목
        ttk.Label(main_frame, text="StepBack", font=("Malgun Gothic", 24, "bold"), 
                foreground="#4A90E2").pack(pady=(0, 20))

        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.Frame(content_frame, padding=(0, 0, 20, 0))
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        right_frame = ttk.Frame(content_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 왼쪽 메뉴 버튼
        ttk.Button(left_frame, text="불안도 체크", command=self.check_anxiety, width=20).pack(pady=5)
        ttk.Button(left_frame, text="기록 보기", command=self.view_records, width=20).pack(pady=5)

        # 목표 섹션
        goals_frame = ttk.LabelFrame(right_frame, text="오늘의 목표", padding=15)
        goals_frame.pack(fill=tk.X, pady=(0, 15))

        # 목표 입력 프레임
        goal_input_frame = ttk.Frame(goals_frame)
        goal_input_frame.pack(fill=tk.X, pady=(0, 10))

        goal_entry = tk.Text(goal_input_frame, width=40, height=1, 
                            font=('Malgun Gothic', 11), bg='#2B2B2B', fg='#CCCCCC')
        goal_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), pady=5)
        ttk.Button(goal_input_frame, text="추가", 
                command=lambda: self.add_goal(goal_entry)).pack(side=tk.RIGHT)

        # 활동 섹션도 같은 방식으로 구성
        activities_frame = ttk.LabelFrame(right_frame, text="오늘의 활동", padding=15)
        activities_frame.pack(fill=tk.X)

        activity_input_frame = ttk.Frame(activities_frame)
        activity_input_frame.pack(fill=tk.X, pady=(0, 10))

        activity_entry = tk.Text(activity_input_frame, width=40, height=1, 
                            font=('Malgun Gothic', 11), bg='#2B2B2B', fg='#CCCCCC')
        activity_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), pady=5)
        ttk.Button(activity_input_frame, text="추가", 
                command=lambda: self.add_activity(activity_entry)).pack(side=tk.RIGHT)



    def create_goal_widget(self, parent, index, goal):
        goal_frame = ttk.Frame(parent)
        goal_frame.pack(fill=tk.X, pady=5)
        
        var = tk.BooleanVar(value=goal['completed'])
        cb = ttk.Checkbutton(goal_frame, variable=var, command=lambda i=index, v=var: self.toggle_goal(i, v))
        cb.pack(side=tk.LEFT)
        
        if goal['completed']:
            goal_text = f"\u0336{goal['text']}\u0336"
        else:
            goal_text = goal['text']
        
        ttk.Label(goal_frame, text=goal_text, wraplength=300).pack(side=tk.LEFT, padx=(5, 10), fill=tk.X, expand=True)
        ttk.Button(goal_frame, text="삭제", width=5, command=lambda i=index: self.delete_goal(i)).pack(side=tk.RIGHT)

    def create_activity_widget(self, parent, index, activity):
        activity_frame = ttk.Frame(parent)
        activity_frame.pack(fill=tk.X, pady=5)
        ttk.Label(activity_frame, text=activity['activity'], wraplength=300).pack(side=tk.LEFT, padx=(5, 10), fill=tk.X, expand=True)
        ttk.Button(activity_frame, text="삭제", width=5, command=lambda i=index: self.delete_activity(i)).pack(side=tk.RIGHT)

    def add_goal(self, entry):
        goal = entry.get("1.0", tk.END).strip()
        if goal:
            self.goals.append({"date": datetime.now().strftime("%Y-%m-%d"), "text": goal, "completed": False})
            self.save_data()
            entry.delete("1.0", tk.END)
            self.create_main_menu()

    def add_activity(self, entry):
        activity = entry.get("1.0", tk.END).strip()
        if activity:
            self.activity_log.append({"date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "activity": activity})
            self.save_data()
            entry.delete("1.0", tk.END)
            self.create_main_menu()

    def check_anxiety(self):
        anxiety_window = tk.Toplevel(self.master)
        anxiety_window.title("불안도 체크")
        anxiety_window.geometry("300x200")
        anxiety_window.configure(bg='#1E1E1E')

        ttk.Label(anxiety_window, text="오늘의 불안 수준", font=("Malgun Gothic", 14)).pack(pady=10)

        self.anxiety_slider = ttk.Scale(
            anxiety_window, from_=1, to=10, orient=tk.HORIZONTAL, length=200,
            command=self.update_anxiety_label
        )
        self.anxiety_slider.set(5)
        self.anxiety_slider.pack(pady=10)

        self.anxiety_label = ttk.Label(anxiety_window, text="현재 불안 수준: 5", font=("Malgun Gothic", 12))
        self.anxiety_label.pack(pady=5)

        ttk.Button(anxiety_window, text="저장", command=lambda: self.save_anxiety(anxiety_window)).pack(pady=10)

    def update_anxiety_label(self, value):
        self.anxiety_label.config(text=f"현재 불안 수준: {int(float(value))}")

    def save_anxiety(self, window):
        anxiety_level = int(self.anxiety_slider.get())
        self.progress_data.append({"date": datetime.now().strftime("%Y-%m-%d"), "score": anxiety_level})
        self.save_data()
        messagebox.showinfo("저장 완료", f"오늘의 불안 수준 {anxiety_level}이 저장되었습니다.")
        window.destroy()
        self.create_main_menu()

    def toggle_goal(self, index, var):
        self.goals[index]['completed'] = var.get()
        self.save_data()
        self.create_main_menu()

    def delete_goal(self, index):
        del self.goals[index]
        self.save_data()
        self.create_main_menu()

    def delete_activity(self, index):
        del self.activity_log[index]
        self.save_data()
        self.create_main_menu()

    def view_records(self):
        records_window = tk.Toplevel(self.master)
        records_window.title("기록 보기")
        records_window.geometry("800x600")
        records_window.configure(bg='#1E1E1E')

        main_frame = ttk.Frame(records_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        records_canvas = tk.Canvas(main_frame, bg='#1E1E1E', highlightthickness=0)
        records_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=records_canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        records_canvas.configure(yscrollcommand=scrollbar.set)
        records_canvas.bind('<Configure>', lambda e: records_canvas.configure(scrollregion=records_canvas.bbox("all")))

        records_frame = ttk.Frame(records_canvas)
        records_canvas.create_window((0, 0), window=records_frame, anchor="nw")

        dates = sorted(set([goal['date'] for goal in self.goals] + 
                           [activity['date'].split()[0] for activity in self.activity_log] + 
                           [data['date'] for data in self.progress_data]), reverse=True)

        # 그래프 스타일 설정
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(10, 4))
        fig.patch.set_facecolor('#1E1E1E')
        ax.set_facecolor('#1E1E1E')
        
        # 그래프 그리기
        ax.plot([datetime.strptime(date, "%Y-%m-%d") for date in dates], 
                [next((data['score'] for data in self.progress_data if data['date'] == date), None) for date in dates],
                marker='o', linestyle='-', color='#4A90E2')
        
        # 그래프 스타일링
        ax.set_title("불안도 변화", fontsize=12, color='#CCCCCC')
        ax.set_xlabel("날짜", fontsize=10, color='#CCCCCC')
        ax.set_ylabel("불안도", fontsize=10, color='#CCCCCC')
        ax.tick_params(colors='#CCCCCC')
        ax.set_ylim(0, 10)
        plt.xticks(rotation=45)
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=records_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=(0, 20))

        for date in dates:
            date_frame = ttk.LabelFrame(records_frame, text=date, padding=10)
            date_frame.pack(fill=tk.X, pady=(0, 20))

            # 목표
            goals = [goal for goal in self.goals if goal['date'] == date]
            if goals:
                ttk.Label(date_frame, text="목표:", font=("Malgun Gothic", 10, "bold")).pack(anchor=tk.W)
                for goal in goals:
                    goal_text = f"{'[완료] ' if goal['completed'] else ''}{goal['text']}"
                    ttk.Label(date_frame, text=goal_text, wraplength=700).pack(anchor=tk.W, padx=(10, 0))

            # 활동
            activities = [activity for activity in self.activity_log if activity['date'].split()[0] == date]
            if activities:
                ttk.Label(date_frame, text="활동:", font=("Malgun Gothic", 10, "bold")).pack(anchor=tk.W, pady=(10, 0))
                for activity in activities:
                    ttk.Label(date_frame, text=activity['activity'], wraplength=700).pack(anchor=tk.W, padx=(10, 0))

    def save_data(self):
        data = {
            "activity_log": self.activity_log,
            "progress_data": self.progress_data,
            "goals": self.goals
        }
        with open("stepback_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

    def load_data(self):
        try:
            with open("stepback_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.activity_log = data.get("activity_log", [])
                self.progress_data = data.get("progress_data", [])
                self.goals = data.get("goals", [])
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = StepBackApp(root)
    root.mainloop()
