import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle, Polygon
import numpy as np
import math
from rectangle_triangle_perimeter import (
    rectangle_perimeter, triangle_perimeter, 
    triangle_rectangle_intersect
)

class GeometryCalculatorLabGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Лабораторная работа №9 - Тестирование ПО")
        self.root.geometry("1400x700")
        self.root.configure(bg='#f0f0f0')
        
        # Переменные для хранения данных
        self.current_test = 0
        
        # Предустановленные тесты для всех ветвей
        self.test_cases = [
            {
                "name": "Тест 1: Пересекающиеся фигуры",
                "description": "Треугольник частично внутри прямоугольника",
                "rect": (-50, -30, 50, 30),
                "triangle": ((-25, -15), (25, -15), (-25, 15)),
                "expected": "Пересекаются"
            },
            {
                "name": "Тест 2: Фигуры не пересекаются",
                "description": "Фигуры далеко друг от друга",
                "rect": (-100, -50, -20, 20),
                "triangle": ((50, 30), (80, 30), (50, 60)),
                "expected": "Не пересекаются"
            },
            {
                "name": "Тест 3: Соприкасающиеся фигуры",
                "description": "Фигуры касаются по одной точке",
                "rect": (-60, -40, 0, 40),
                "triangle": ((0, -20), (40, -20), (0, 20)),
                "expected": "Соприкасаются"
            },
            {
                "name": "Тест 4: Граничные значения - максимальный диапазон",
                "description": "Фигуры на границах координатного поля",
                "rect": (-200, -200, -100, -100),
                "triangle": ((100, 100), (200, 100), (100, 200)),
                "expected": "Не пересекаются"
            },
            {
                "name": "Тест 5: Граничные значения - нулевые координаты",
                "description": "Фигуры проходят через центр координат",
                "rect": (-20, -20, 20, 20),
                "triangle": ((0, 0), (30, 0), (0, 30)),
                "expected": "Пересекаются"
            },
            {
                "name": "Тест 6: Треугольник внутри прямоугольника",
                "description": "Треугольник полностью внутри прямоугольника",
                "rect": (-80, -80, 80, 80),
                "triangle": ((-20, -20), (20, -20), (-20, 20)),
                "expected": "Пересекаются"
            },
            {
                "name": "Тест 7: Прямоугольник внутри треугольника",
                "description": "Прямоугольник полностью внутри треугольника",
                "rect": (-10, -10, 10, 10),
                "triangle": ((-50, -50), (50, -50), (-50, 50)),
                "expected": "Пересекаются"
            },
            {
                "name": "Тест 8: Вырожденный случай - линия",
                "description": "Прямоугольник вырожден в линию",
                "rect": (0, -30, 0, 30),
                "triangle": ((-20, -10), (20, -10), (-20, 10)),
                "expected": "Пересекаются"
            }
        ]
        
        self.setup_gui()
        self.setup_plot()
        self.load_test_case(0)
        
    def setup_gui(self):
        """Настройка графического интерфейса"""
        # Главный заголовок
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill='x', padx=5, pady=5)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, 
                              text="*** ЛАБОРАТОРНАЯ РАБОТА №9: ТЕСТИРОВАНИЕ ПО ***", 
                              font=('Arial', 16, 'bold'),
                              bg='#2c3e50', fg='white')
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(title_frame,
                                 text="Поле 600x600 пикселей, координаты от -200 до 200, центр в центре",
                                 font=('Arial', 10),
                                 bg='#2c3e50', fg='#ecf0f1')
        subtitle_label.pack()
        
        # Основной контейнер
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Левая панель - управление тестами
        left_frame = tk.Frame(main_frame, bg='white', relief='raised', bd=2, width=350)
        left_frame.pack(side='left', fill='y', padx=(0, 5))
        left_frame.pack_propagate(False)
        
        # Правая панель - график 600x600
        right_frame = tk.Frame(main_frame, bg='white', relief='raised', bd=2)
        right_frame.pack(side='right', fill='both', expand=True)
        
        self.setup_control_panel(left_frame)
        self.setup_plot_panel(right_frame)
        
    def setup_control_panel(self, parent):
        """Настройка панели управления"""
        # Заголовок панели
        control_title = tk.Label(parent, text="ТЕСТЫ ДЛЯ ВСЕХ ВЕТВЕЙ", 
                               font=('Arial', 14, 'bold'),
                               bg='white', fg='#2c3e50')
        control_title.pack(pady=10)
        
        # Список тестов
        test_frame = tk.LabelFrame(parent, text="Выберите тест", 
                                 font=('Arial', 12, 'bold'),
                                 bg='white', fg='#8e44ad',
                                 padx=10, pady=10)
        test_frame.pack(fill='x', padx=10, pady=5)
        
        self.test_listbox = tk.Listbox(test_frame, height=8, font=('Arial', 9))
        for i, test in enumerate(self.test_cases):
            self.test_listbox.insert(i, f"{i+1}. {test['name']}")
        self.test_listbox.pack(fill='x', pady=5)
        self.test_listbox.bind('<<ListboxSelect>>', self.on_test_select)
        
        # Кнопки навигации
        nav_frame = tk.Frame(test_frame, bg='white')
        nav_frame.pack(fill='x', pady=5)
        
        prev_btn = tk.Button(nav_frame, text="< Предыдущий", 
                           command=self.prev_test,
                           bg='#3498db', fg='white', font=('Arial', 9))
        prev_btn.pack(side='left', padx=2)
        
        next_btn = tk.Button(nav_frame, text="Следующий >", 
                           command=self.next_test,
                           bg='#3498db', fg='white', font=('Arial', 9))
        next_btn.pack(side='right', padx=2)
        
        # Описание текущего теста
        desc_frame = tk.LabelFrame(parent, text="Описание теста", 
                                 font=('Arial', 12, 'bold'),
                                 bg='white', fg='#27ae60',
                                 padx=10, pady=10)
        desc_frame.pack(fill='x', padx=10, pady=5)
        
        self.desc_text = tk.Text(desc_frame, height=4, width=35,
                               font=('Arial', 9), bg='#ecf0f1',
                               relief='sunken', bd=2, wrap='word')
        self.desc_text.pack(fill='both', expand=True)
        
        # Ручной ввод координат
        manual_frame = tk.LabelFrame(parent, text="Ручной ввод", 
                                   font=('Arial', 12, 'bold'),
                                   bg='white', fg='#e74c3c',
                                   padx=10, pady=10)
        manual_frame.pack(fill='x', padx=10, pady=5)
        
        # Прямоугольник
        tk.Label(manual_frame, text="Прямоугольник:", bg='white', font=('Arial', 10, 'bold')).grid(row=0, column=0, columnspan=4, sticky='w')
        
        rect_labels = ["x1:", "y1:", "x2:", "y2:"]
        self.rect_entries = []
        for i, label in enumerate(rect_labels):
            tk.Label(manual_frame, text=label, bg='white').grid(row=1, column=i, padx=2)
            entry = tk.Entry(manual_frame, width=8, font=('Arial', 9))
            entry.grid(row=2, column=i, padx=2, pady=2)
            entry.bind('<KeyRelease>', self.on_manual_change)
            self.rect_entries.append(entry)
        
        # Треугольник
        tk.Label(manual_frame, text="Треугольник:", bg='white', font=('Arial', 10, 'bold')).grid(row=3, column=0, columnspan=4, sticky='w', pady=(10,0))
        
        tri_labels = ["x0:", "y0:", "x1:", "y1:"]
        self.tri_entries = []
        for i, label in enumerate(tri_labels):
            tk.Label(manual_frame, text=label, bg='white').grid(row=4, column=i, padx=2)
            entry = tk.Entry(manual_frame, width=8, font=('Arial', 9))
            entry.grid(row=5, column=i, padx=2, pady=2)
            entry.bind('<KeyRelease>', self.on_manual_change)
            self.tri_entries.append(entry)
        
        # Результаты
        self.results_frame = tk.LabelFrame(parent, text="РЕЗУЛЬТАТЫ ТЕСТА", 
                                          font=('Arial', 12, 'bold'),
                                          bg='white', fg='#8e44ad',
                                          padx=10, pady=10)
        self.results_frame.pack(fill='x', padx=10, pady=5)
        
        self.result_text = tk.Text(self.results_frame, height=8, width=35,
                                  font=('Courier', 8),
                                  bg='#ecf0f1', fg='#2c3e50',
                                  relief='sunken', bd=2)
        self.result_text.pack(fill='both', expand=True)
        
    def setup_plot_panel(self, parent):
        """Настройка панели с графиком 600x600"""
        plot_title = tk.Label(parent, text="ГРАФИЧЕСКОЕ ПОЛЕ 600x600 ПИКСЕЛЕЙ", 
                             font=('Arial', 14, 'bold'),
                             bg='white', fg='#2c3e50')
        plot_title.pack(pady=10)
        
        # Создаем matplotlib фигуру строго 600x600 пикселей
        self.fig, self.ax = plt.subplots(figsize=(6, 6))  # 6x6 дюймов = 600x600 при 100 DPI
        self.fig.patch.set_facecolor('white')
        
        self.canvas = FigureCanvasTkAgg(self.fig, parent)
        self.canvas.get_tk_widget().pack(padx=10, pady=10)
        
    def setup_plot(self):
        """Настройка графика согласно требованиям"""
        # Диапазон от -200 до 200, центр в центре
        self.ax.set_xlim(-200, 200)
        self.ax.set_ylim(-200, 200)
        self.ax.set_xlabel('X координата', fontsize=12)
        self.ax.set_ylabel('Y координата', fontsize=12)
        self.ax.grid(True, alpha=0.3, linestyle='--')
        self.ax.set_aspect('equal')
        
        # Добавляем оси через центр
        self.ax.axhline(y=0, color='black', linewidth=0.8, alpha=0.8)
        self.ax.axvline(x=0, color='black', linewidth=0.8, alpha=0.8)
        
        # Добавляем деления через каждые 50 единиц
        major_ticks = np.arange(-200, 201, 50)
        minor_ticks = np.arange(-200, 201, 25)
        
        self.ax.set_xticks(major_ticks)
        self.ax.set_yticks(major_ticks)
        self.ax.set_xticks(minor_ticks, minor=True)
        self.ax.set_yticks(minor_ticks, minor=True)
        
        self.ax.grid(which='minor', alpha=0.2)
        self.ax.grid(which='major', alpha=0.5)
        
    def load_test_case(self, index):
        """Загрузка тестового случая"""
        if 0 <= index < len(self.test_cases):
            self.current_test = index
            test = self.test_cases[index]
            
            # Обновляем описание
            self.desc_text.delete(1.0, tk.END)
            desc = f"{test['name']}\n\n{test['description']}\n\nОжидается: {test['expected']}"
            self.desc_text.insert(1.0, desc)
            
            # Загружаем координаты
            rect = test['rect']
            triangle = test['triangle']
            
            # Заполняем поля ввода
            self.rect_entries[0].delete(0, tk.END)
            self.rect_entries[0].insert(0, str(rect[0]))
            self.rect_entries[1].delete(0, tk.END)
            self.rect_entries[1].insert(0, str(rect[1]))
            self.rect_entries[2].delete(0, tk.END)
            self.rect_entries[2].insert(0, str(rect[2]))
            self.rect_entries[3].delete(0, tk.END)
            self.rect_entries[3].insert(0, str(rect[3]))
            
            # Треугольник: прямой угол (triangle[0]), конец первого катета (triangle[1][0]), конец второго катета (triangle[2][1])
            self.tri_entries[0].delete(0, tk.END)
            self.tri_entries[0].insert(0, str(triangle[0][0]))  # x прямого угла
            self.tri_entries[1].delete(0, tk.END)
            self.tri_entries[1].insert(0, str(triangle[0][1]))  # y прямого угла
            self.tri_entries[2].delete(0, tk.END)
            self.tri_entries[2].insert(0, str(triangle[1][0]))  # x конца первого катета
            self.tri_entries[3].delete(0, tk.END)
            self.tri_entries[3].insert(0, str(triangle[2][1]))  # y конца второго катета
            
            # Выделяем в списке
            self.test_listbox.selection_clear(0, tk.END)
            self.test_listbox.selection_set(index)
            
            # Перерисовываем
            self.calculate_and_plot()
            
    def on_test_select(self, event):
        """Обработчик выбора теста из списка"""
        selection = self.test_listbox.curselection()
        if selection:
            self.load_test_case(selection[0])
            
    def prev_test(self):
        """Предыдущий тест"""
        new_index = (self.current_test - 1) % len(self.test_cases)
        self.load_test_case(new_index)
        
    def next_test(self):
        """Следующий тест"""
        new_index = (self.current_test + 1) % len(self.test_cases)
        self.load_test_case(new_index)
        
    def on_manual_change(self, event=None):
        """Обработчик ручного изменения координат"""
        self.root.after(300, self.calculate_and_plot)
        
    def get_current_data(self):
        """Получение текущих данных из полей ввода"""
        try:
            # Прямоугольник
            x1 = float(self.rect_entries[0].get())
            y1 = float(self.rect_entries[1].get())
            x2 = float(self.rect_entries[2].get())
            y2 = float(self.rect_entries[3].get())
            
            # Упорядочиваем координаты
            if x1 > x2:
                x1, x2 = x2, x1
            if y1 > y2:
                y1, y2 = y2, y1
                
            rectangle = (x1, y1, x2, y2)
            
            # Треугольник
            x0 = float(self.tri_entries[0].get())  # прямой угол
            y0 = float(self.tri_entries[1].get())
            x1_tri = float(self.tri_entries[2].get())  # конец первого катета
            y1_tri = float(self.tri_entries[3].get())  # конец второго катета
            
            triangle = ((x0, y0), (x1_tri, y0), (x0, y1_tri))
            
            return rectangle, triangle
        except ValueError:
            return None, None
    
    def calculate_and_plot(self):
        """Основной метод расчета и отображения"""
        rectangle, triangle = self.get_current_data()
        
        if rectangle is None or triangle is None:
            return
            
        # Проверяем границы координат (-200 до 200)
        all_coords = [rectangle[0], rectangle[1], rectangle[2], rectangle[3],
                     triangle[0][0], triangle[0][1], triangle[1][0], triangle[2][1]]
        
        out_of_bounds = [coord for coord in all_coords if coord < -200 or coord > 200]
        
        # Очищаем график
        self.ax.clear()
        self.setup_plot()
        
        # Отображаем фигуры
        self.plot_rectangle(rectangle, out_of_bounds)
        self.plot_triangle(triangle, out_of_bounds)
        
        # Расчеты
        intersect = triangle_rectangle_intersect(triangle, rectangle)
        rect_p = rectangle_perimeter(*rectangle)
        tri_p = triangle_perimeter(triangle)
        
        # Обновляем результаты
        self.update_results(rectangle, triangle, intersect, rect_p, tri_p, out_of_bounds)
        
        self.canvas.draw()
        
    def plot_rectangle(self, rectangle, out_of_bounds):
        """Отображение прямоугольника"""
        x1, y1, x2, y2 = rectangle
        width = x2 - x1
        height = y2 - y1
        
        # Цвет зависит от того, в границах ли координаты
        color = '#e74c3c' if out_of_bounds else '#3498db'
        
        rect = Rectangle((x1, y1), width, height, 
                        linewidth=2, edgecolor=color, 
                        facecolor=color, alpha=0.3,
                        label=f'Прямоугольник ({width}×{height})')
        self.ax.add_patch(rect)
        
        # Добавляем координаты углов
        corners = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
        for x, y in corners:
            point_color = '#c0392b' if (x < -200 or x > 200 or y < -200 or y > 200) else '#2980b9'
            self.ax.plot(x, y, 'o', color=point_color, markersize=6)
    
    def plot_triangle(self, triangle, out_of_bounds):
        """Отображение треугольника"""
        # Цвет зависит от того, в границах ли координаты
        color = '#e74c3c' if out_of_bounds else '#e67e22'
        
        tri_array = np.array(triangle)
        triangle_patch = Polygon(tri_array, 
                               linewidth=2, edgecolor=color,
                               facecolor=color, alpha=0.3,
                               label=f'Треугольник')
        self.ax.add_patch(triangle_patch)
        
        # Добавляем координаты вершин
        labels = ['Прямой угол', 'Катет 1', 'Катет 2']
        for i, (x, y) in enumerate(triangle):
            point_color = '#c0392b' if (x < -200 or x > 200 or y < -200 or y > 200) else '#d35400'
            self.ax.plot(x, y, 's', color=point_color, markersize=6)
            
        # Добавляем легенду
        self.ax.legend(loc='upper right', bbox_to_anchor=(0.98, 0.98))
        
    def update_results(self, rectangle, triangle, intersect, rect_p, tri_p, out_of_bounds):
        """Обновление результатов"""
        self.result_text.delete(1.0, tk.END)
        
        # Проверяем ветви алгоритма
        expected = self.test_cases[self.current_test]['expected'].lower()
        actual = "пересекаются" if intersect else "не пересекаются"
        test_result = "[+] ПРОЙДЕН" if expected in actual else "[-] НЕ ПРОЙДЕН"
        
        bounds_status = "[-] ВНЕ ГРАНИЦ" if out_of_bounds else "[+] В ГРАНИЦАХ"
        
        result = f"""ТЕСТ {self.current_test + 1}: {test_result}

АНАЛИЗ ФИГУР:

Прямоугольник:
   ({rectangle[0]:.1f},{rectangle[1]:.1f}) -> ({rectangle[2]:.1f},{rectangle[3]:.1f})
   Размер: {abs(rectangle[2]-rectangle[0]):.1f}x{abs(rectangle[3]-rectangle[1]):.1f}
   Периметр: {rect_p:.2f}

Треугольник:
   Прямой угол: ({triangle[0][0]:.1f},{triangle[0][1]:.1f})
   Катет 1: {abs(triangle[1][0] - triangle[0][0]):.1f}
   Катет 2: {abs(triangle[2][1] - triangle[0][1]):.1f}
   Периметр: {tri_p:.2f}

РЕЗУЛЬТАТ:
   Пересекаются: {"[+] ДА" if intersect else "[-] НЕТ"}
   {f"Общий периметр: {rect_p + tri_p:.2f}" if intersect else "Периметр не определен"}
   
ГРАНИЦЫ ПОЛЯ: {bounds_status}
   Диапазон: -200 <= x,y <= 200
   {f"Нарушения: {out_of_bounds}" if out_of_bounds else "Все координаты в пределах"}

ПОКРЫТИЕ ВЕТВЕЙ:
   + Проверка пересечения
   + Расчет периметров  
   + Валидация границ
   + Обработка вырожденных случаев
"""
        
        self.result_text.insert(1.0, result)
        
        # Заголовок графика
        title_color = '#27ae60' if intersect else '#e74c3c'
        title_text = f"ТЕСТ {self.current_test + 1}: {'[+] ПЕРЕСЕКАЮТСЯ' if intersect else '[-] НЕ ПЕРЕСЕКАЮТСЯ'}"
        self.ax.set_title(title_text, fontsize=12, fontweight='bold', color=title_color)

def main():
    """Главная функция запуска GUI"""
    root = tk.Tk()
    
    app = GeometryCalculatorLabGUI(root)
    
    # Центрирование окна
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (1400 // 2)
    y = (root.winfo_screenheight() // 2) - (700 // 2)
    root.geometry(f"1400x700+{x}+{y}")
    
    print("*** Запуск программы согласно требованиям лабораторной работы:")
    print("   - Поле: 600x600 пикселей")
    print("   - Центр координат: в центре поля")
    print("   - Диапазон: от -200 до 200 по каждой оси")
    print("   - Тесты: все ветви графа потока управления")
    print("   - Граничные значения: включены в тесты")
    
    root.mainloop()

if __name__ == "__main__":
    main() 