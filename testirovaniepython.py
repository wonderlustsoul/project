import tkinter as tk
from tkinter import messagebox, ttk

# ----- Блок логики и данных -----
questions = []
current_index = 0
score = 0
student_name = ""
student_group = ""
answer_var = None  # создадим после root

def add_question_to_store(question_text, options, correct_index):
    questions.append({
        "question": question_text,
        "options": options,
        "correct": correct_index
    })

def check_answer(idx, answer_idx):
    global score
    if questions[idx]["correct"] == answer_idx:
        score += 1
        return True
    return False

def reset_test():
    global current_index, score
    current_index = 0
    score = 0

def next_idx():
    global current_index
    current_index += 1
    return current_index

def prev_idx():
    global current_index
    current_index -= 1
    return current_index

def calculate_grade():
    total = len(questions)
    pct = (score / total) * 100 if total else 0
    if pct >= 85:
        return "Отлично! (5)"
    elif pct >= 70:
        return "Хорошо! (4)"
    elif pct >= 50:
        return "Удовлетворительно (3)"
    return "Неудовлетворительно (2)"

# ----- Функции для работы меню -----
def on_exit():
    root.destroy()

def show_about():
    messagebox.showinfo("О программе", "Простая система тестирования на Tkinter.\nАвторы: Ернур и Бекжан")

# ----- Функции для экранов интерфейса в табах -----
def add_question():
    """ Обработчик кнопки 'Добавить вопрос' в табе преподавателя """
    q_text = question_entry.get("1.0", "end-1c").strip()
    if not q_text:
        messagebox.showerror("Ошибка", "Введите текст вопроса!")
        return
    opts = []
    for e in option_entries:
        o = e.get().strip()
        if not o:
            messagebox.showerror("Ошибка", "Все варианты ответов должны быть заполнены!")
            return
        opts.append(o)
    ci = correct_var.get()
    if ci == -1:
        messagebox.showerror("Ошибка", "Выберите правильный ответ!")
        return
    add_question_to_store(q_text, opts, ci)
    messagebox.showinfo("Успех", f"Вопрос добавлен! Всего вопросов: {len(questions)}")
    clear_form()

def clear_form():
    """ Обнуление полей ввода в табе преподавателя """
    question_entry.delete("1.0", "end")
    for e in option_entries:
        e.delete(0, "end")
    correct_var.set(-1)
    label_q_count.config(text=f"Вопросов добавлено: {len(questions)}")

# ----- Функции для студента в одном табе -----
def start_test():
    """ Проверка данных студента и запуск теста """
    global student_name, student_group
    student_name = name_entry.get().strip()
    student_group = group_entry.get().strip()
    if not student_name or not student_group:
        messagebox.showerror("Ошибка", "Заполните все поля (Имя и Группа)!")
        return
    if not questions:
        messagebox.showerror("Ошибка", "Нет доступных вопросов для теста!")
        return
    reset_test()
    login_frame.pack_forget()
    show_question_screen()

def show_question_screen():
    """ Отображает текущий вопрос и варианты в quiz_frame """
    for w in quiz_frame.winfo_children():
        w.destroy()

    qdata = questions[current_index]
    quiz_frame.config(bg=student_bg)
    quiz_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Контейнер для вопроса
    question_container = tk.Frame(quiz_frame, bg=student_bg)
    question_container.pack(fill="both", expand=True, padx=20, pady=10)
    
    tk.Label(
        question_container,
        text=qdata["question"],
        font=("Arial", 12),
        wraplength=600,
        justify="left",
        bg=student_bg
    ).pack(pady=10, anchor="w", fill="x", expand=True)

    # Контейнер для вариантов ответа
    options_container = tk.Frame(quiz_frame, bg=student_bg)
    options_container.pack(fill="both", expand=True, padx=20, pady=5)

    answer_var.set(-1)
    for i, opt in enumerate(qdata["options"]):
        rb = tk.Radiobutton(
            options_container,
            text=opt,
            variable=answer_var,
            value=i,
            wraplength=580,
            justify="left",
            bg=student_bg,
            anchor="w"
        )
        rb.pack(fill="x", padx=20, pady=5, anchor="w", expand=True)

    # Контейнер для навигации
    nav = tk.Frame(quiz_frame, bg=student_bg)
    nav.pack(pady=15, fill="x", padx=20)

    def go_prev():
        global score
        # Если возвращаемся назад и предыдущий ответ был верным — уменьшаем счёт
        if answer_var.get() == questions[current_index]["correct"]:
            score -= 1
        prev_idx()
        show_question_screen()

    def go_next():
        if answer_var.get() == -1:
            messagebox.showwarning("Предупреждение", "Выберите вариант ответа!")
            return
        check_answer(current_index, answer_var.get())
        next_idx()
        show_question_screen()

    def finish_test_wrapper():
        if answer_var.get() == -1:
            messagebox.showwarning("Предупреждение", "Выберите вариант ответа!")
            return
        check_answer(current_index, answer_var.get())
        show_results_screen()

    # Кнопки навигации
    if current_index > 0:
        tk.Button(nav, text="Назад", command=go_prev, width=10).pack(side="left", padx=5)
    if current_index < len(questions) - 1:
        tk.Button(nav, text="Далее", command=go_next, width=10).pack(side="right", padx=5)
    else:
        tk.Button(nav, text="Завершить тест", command=finish_test_wrapper, width=12).pack(side="right", padx=5)

def show_results_screen():
    """ Отображает результаты теста """
    for w in quiz_frame.winfo_children():
        w.destroy()
    quiz_frame.pack_forget()

    result_frame.config(bg=student_bg)
    result_frame.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(
        result_frame,
        text="Результаты тестирования",
        font=("Arial", 16, "bold"),
        bg=student_bg
    ).pack(pady=15)
    
    tk.Label(
        result_frame, 
        text=f"Студент: {student_name}", 
        font=("Arial", 12),
        bg=student_bg
    ).pack(pady=5)
    
    tk.Label(
        result_frame, 
        text=f"Группа: {student_group}", 
        font=("Arial", 12),
        bg=student_bg
    ).pack(pady=5)
    
    tk.Label(
        result_frame,
        text=f"\nВаш результат: {score} из {len(questions)}",
        font=("Arial", 14),
        bg=student_bg
    ).pack(pady=15)

    grade = calculate_grade()
    tk.Label(
        result_frame, 
        text=grade, 
        font=("Arial", 14, "bold"),
        bg=student_bg
    ).pack(pady=10)

    tk.Button(
        result_frame, 
        text="Вернуться к входу", 
        command=restart_student, 
        width=15,
        height=2
    ).pack(pady=20)

def restart_student():
    """ Возвращает студента к форме логина, очищает результаты """
    global current_index, score
    current_index = 0
    score = 0
    result_frame.pack_forget()
    login_frame.pack(fill="both", expand=True, padx=20, pady=20)

# ----- Основной запуск -----
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Система тестирования")
    
    # Установка полноэкранного режима
    root.attributes('-fullscreen', True)
    # Альтернатива: root.state('zoomed') для развернутого окна без панели задач
    
    # Разрешаем изменение размеров
    root.resizable(True, True)
    
    # Задаём фоновый цвет для всего окна
    bg_color = "#F0F8FF"       # светло-голубой
    teacher_bg = "#FFF8DC"     # кремовый для вкладки Преподавателя
    student_bg = "#F5FFFA"     # мятный для вкладки Студента
    root.configure(bg=bg_color)
    
    # Устанавливаем минимальный размер окна
    root.minsize(800, 600)

    # Создаём меню
    menubar = tk.Menu(root)
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Выход", command=on_exit)
    menubar.add_cascade(label="Файл", menu=file_menu)

    help_menu = tk.Menu(menubar, tearoff=0)
    help_menu.add_command(label="О программе", command=show_about)
    menubar.add_cascade(label="Помощь", menu=help_menu)

    root.config(menu=menubar)

    # Создаём Notebook с двумя вкладками
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    # ----- Вкладка "Преподаватель" -----
    teacher_frame = tk.Frame(notebook, bg=teacher_bg)
    notebook.add(teacher_frame, text="Преподаватель")
    
    # Контейнер для содержимого с отступами
    teacher_content = tk.Frame(teacher_frame, bg=teacher_bg, padx=20, pady=20)
    teacher_content.pack(fill="both", expand=True)

    # Надпись "Добавление вопросов"
    tk.Label(teacher_content, text="Добавление вопросов", font=("Arial", 16), bg=teacher_bg).pack(pady=15, anchor="w")

    # Поле для текста вопроса
    tk.Label(teacher_content, text="Вопрос:", bg=teacher_bg, font=("Arial", 11)).pack(anchor="w", pady=(5, 0))
    question_entry = tk.Text(teacher_content, height=4, width=80, font=("Arial", 11))
    question_entry.pack(fill="x", pady=5, padx=(0, 10))

    # Поля для пяти вариантов ответов
    tk.Label(teacher_content, text="Варианты ответов:", bg=teacher_bg, font=("Arial", 11)).pack(anchor="w", pady=(15, 0))
    option_entries = []
    for i in range(5):
        frame_opt = tk.Frame(teacher_content, bg=teacher_bg)
        frame_opt.pack(fill="x", pady=5)
        tk.Label(frame_opt, text=f"{i+1}.", bg=teacher_bg, font=("Arial", 11)).pack(side="left")
        entry = tk.Entry(frame_opt, width=80, bg="white", font=("Arial", 11))
        entry.pack(side="left", padx=5, fill="x", expand=True)
        option_entries.append(entry)

    # Радиокнопки для выбора правильного ответа
    tk.Label(teacher_content, text="Правильный ответ:", bg=teacher_bg, font=("Arial", 11)).pack(anchor="w", pady=(15, 0))
    correct_var = tk.IntVar(value=-1)
    radioframe = tk.Frame(teacher_content, bg=teacher_bg)
    radioframe.pack(anchor="w", pady=5)
    for i in range(5):
        tk.Radiobutton(
            radioframe, 
            text=f"{i+1}", 
            variable=correct_var, 
            value=i, 
            bg=teacher_bg,
            font=("Arial", 11)
        ).pack(side="left", padx=15)

    # Метка с количеством добавленных вопросов
    label_q_count = tk.Label(teacher_content, text="Вопросов добавлено: 0", bg=teacher_bg, font=("Arial", 11))
    label_q_count.pack(anchor="w", pady=(15, 5))

    # Кнопки для действий в режиме преподавателя
    teacher_btn_frame = tk.Frame(teacher_content, bg=teacher_bg)
    teacher_btn_frame.pack(pady=20, fill="x")
    tk.Button(
        teacher_btn_frame, 
        text="Добавить вопрос", 
        command=add_question, 
        width=15,
        height=2,
        font=("Arial", 11)
    ).pack(side="left", padx=10)
    
    tk.Button(
        teacher_btn_frame, 
        text="Очистить форму", 
        command=clear_form, 
        width=15,
        height=2,
        font=("Arial", 11)
    ).pack(side="left", padx=10)

    # ----- Вкладка "Студент" -----
    student_frame = tk.Frame(notebook, bg=student_bg)
    notebook.add(student_frame, text="Студент")

    # --- Блок логина студента ---
    login_frame = tk.Frame(student_frame, bg=student_bg)
    login_frame.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(
        login_frame, 
        text="Введите ваши данные", 
        font=("Arial", 16),
        bg=student_bg
    ).pack(pady=20)
    
    input_frame = tk.Frame(login_frame, bg=student_bg)
    input_frame.pack(pady=20, fill="x", expand=True)

    tk.Label(
        input_frame, 
        text="Имя:", 
        bg=student_bg,
        font=("Arial", 12)
    ).grid(row=0, column=0, padx=10, pady=15, sticky="e")
    
    name_entry = tk.Entry(
        input_frame, 
        width=40, 
        bg="white",
        font=("Arial", 12)
    )
    name_entry.grid(row=0, column=1, padx=10, pady=15, sticky="we")

    tk.Label(
        input_frame, 
        text="Группа:", 
        bg=student_bg,
        font=("Arial", 12)
    ).grid(row=1, column=0, padx=10, pady=15, sticky="e")
    
    group_entry = tk.Entry(
        input_frame, 
        width=40, 
        bg="white",
        font=("Arial", 12)
    )
    group_entry.grid(row=1, column=1, padx=10, pady=15, sticky="we")

    # Настройка колонок для расширения
    input_frame.columnconfigure(1, weight=1)

    btn_frame = tk.Frame(login_frame, bg=student_bg)
    btn_frame.pack(pady=30)
    
    tk.Button(
        btn_frame, 
        text="Начать тест", 
        command=start_test, 
        width=15,
        height=2,
        font=("Arial", 12)
    ).pack(side="left", padx=20)
    
    tk.Button(
        btn_frame, 
        text="Очистить поля", 
        command=lambda: (name_entry.delete(0, "end"), group_entry.delete(0, "end")), 
        width=15,
        height=2,
        font=("Arial", 12)
    ).pack(side="left", padx=20)

    # --- Блок вопросов (скрыт до начала теста) ---
    quiz_frame = tk.Frame(student_frame, bg=student_bg)

    # --- Блок результатов (скрыт до завершения теста) ---
    result_frame = tk.Frame(student_frame, bg=student_bg)

    # Переменная для хранения выбора ответа (создаём после root)
    answer_var = tk.IntVar(value=-1)

    # Запускаем главный цикл
    root.mainloop()
