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

class GeometryCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔧 Калькулятор периметра фигур - Лабораторная работа №9")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Переменные для хранения данных
        self.rect_vars = {}
        self.tri_vars = {}
        
        self.setup_gui()
        self.setup_plot()
        
    def setup_gui(self):
        """Настройка графического интерфейса"""
        # Главный заголовок
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill='x', padx=5, pady=5)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, 
                              text="🎯 РАСЧЕТ ОБЩЕГО ПЕРИМЕТРА ФИГУР", 
                              font=('Arial', 16, 'bold'),
                              bg='#2c3e50', fg='white')
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(title_frame,
                                 text="Лабораторная работа по тестированию ПО - Визуализация и расчеты",
                                 font=('Arial', 10),
                                 bg='#2c3e50', fg='#ecf0f1')
        subtitle_label.pack()
        
        # Основной контейнер
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Левая панель - ввод данных
        left_frame = tk.Frame(main_frame, bg='white', relief='raised', bd=2)
        left_frame.pack(side='left', fill='y', padx=(0, 5))
        
        # Правая панель - график
        right_frame = tk.Frame(main_frame, bg='white', relief='raised', bd=2)
        right_frame.pack(side='right', fill='both', expand=True)
        
        self.setup_input_panel(left_frame)
        self.setup_plot_panel(right_frame)
        
    def setup_input_panel(self, parent):
        """Настройка панели ввода данных"""
        # Заголовок панели
        input_title = tk.Label(parent, text="📋 ВВОД КООРДИНАТ", 
                              font=('Arial', 14, 'bold'),
                              bg='white', fg='#2c3e50')
        input_title.pack(pady=10)
        
        # Секция прямоугольника
        rect_frame = tk.LabelFrame(parent, text="📐 Прямоугольник", 
                                  font=('Arial', 12, 'bold'),
                                  bg='white', fg='#3498db',
                                  padx=10, pady=10)
        rect_frame.pack(fill='x', padx=10, pady=5)
        
        # Поля ввода для прямоугольника
        rect_labels = [
            ("x1 (левый нижний):", "rect_x1", "0"),
            ("y1 (левый нижний):", "rect_y1", "0"), 
            ("x2 (правый верхний):", "rect_x2", "4"),
            ("y2 (правый верхний):", "rect_y2", "3")
        ]
        
        for i, (label, var_name, default) in enumerate(rect_labels):
            tk.Label(rect_frame, text=label, bg='white').grid(row=i, column=0, sticky='w', pady=2)
            var = tk.StringVar(value=default)
            self.rect_vars[var_name] = var
            entry = tk.Entry(rect_frame, textvariable=var, width=10)
            entry.grid(row=i, column=1, padx=(5, 0), pady=2)
            entry.bind('<KeyRelease>', self.on_data_change)
        
        # Секция треугольника
        tri_frame = tk.LabelFrame(parent, text="📐 Прямоугольный треугольник", 
                                 font=('Arial', 12, 'bold'),
                                 bg='white', fg='#e74c3c',
                                 padx=10, pady=10)
        tri_frame.pack(fill='x', padx=10, pady=5)
        
        # Поля ввода для треугольника
        tri_labels = [
            ("x прямого угла:", "tri_x0", "1"),
            ("y прямого угла:", "tri_y0", "1"),
            ("x конца 1-го катета:", "tri_x1", "3"),
            ("y конца 2-го катета:", "tri_y1", "3")
        ]
        
        for i, (label, var_name, default) in enumerate(tri_labels):
            tk.Label(tri_frame, text=label, bg='white').grid(row=i, column=0, sticky='w', pady=2)
            var = tk.StringVar(value=default)
            self.tri_vars[var_name] = var
            entry = tk.Entry(tri_frame, textvariable=var, width=10)
            entry.grid(row=i, column=1, padx=(5, 0), pady=2)
            entry.bind('<KeyRelease>', self.on_data_change)
        
        # Кнопки управления
        button_frame = tk.Frame(parent, bg='white')
        button_frame.pack(fill='x', padx=10, pady=10)
        
        calc_button = tk.Button(button_frame, text="🔄 Пересчитать", 
                               command=self.calculate_and_plot,
                               bg='#27ae60', fg='white', 
                               font=('Arial', 10, 'bold'),
                               relief='raised', bd=3)
        calc_button.pack(fill='x', pady=2)
        
        clear_button = tk.Button(button_frame, text="🗑️ Очистить", 
                                command=self.clear_data,
                                bg='#e67e22', fg='white',
                                font=('Arial', 10, 'bold'),
                                relief='raised', bd=3)
        clear_button.pack(fill='x', pady=2)
        
        # Результаты
        self.results_frame = tk.LabelFrame(parent, text="📊 РЕЗУЛЬТАТЫ", 
                                          font=('Arial', 12, 'bold'),
                                          bg='white', fg='#8e44ad',
                                          padx=10, pady=10)
        self.results_frame.pack(fill='x', padx=10, pady=5)
        
        self.result_text = tk.Text(self.results_frame, height=10, width=30,
                                  font=('Courier', 9),
                                  bg='#ecf0f1', fg='#2c3e50',
                                  relief='sunken', bd=2)
        self.result_text.pack(fill='both', expand=True)
        
    def setup_plot_panel(self, parent):
        """Настройка панели с графиком"""
        plot_title = tk.Label(parent, text="📈 ВИЗУАЛИЗАЦИЯ ФИГУР", 
                             font=('Arial', 14, 'bold'),
                             bg='white', fg='#2c3e50')
        plot_title.pack(pady=10)
        
        # Создаем matplotlib фигуру
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.fig.patch.set_facecolor('white')
        
        self.canvas = FigureCanvasTkAgg(self.fig, parent)
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
        
    def setup_plot(self):
        """Начальная настройка графика"""
        self.ax.set_xlim(-1, 6)
        self.ax.set_ylim(-1, 5)
        self.ax.set_xlabel('X координата', fontsize=12)
        self.ax.set_ylabel('Y координата', fontsize=12)
        self.ax.grid(True, alpha=0.3)
        self.ax.set_aspect('equal')
        self.ax.set_title('Прямоугольник и треугольник', fontsize=14, fontweight='bold')
        
        # Начальный расчет и отображение
        self.calculate_and_plot()
        
    def get_rectangle_coords(self):
        """Получить координаты прямоугольника"""
        try:
            x1 = float(self.rect_vars['rect_x1'].get())
            y1 = float(self.rect_vars['rect_y1'].get())
            x2 = float(self.rect_vars['rect_x2'].get())
            y2 = float(self.rect_vars['rect_y2'].get())
            
            # Упорядочиваем координаты
            if x1 > x2:
                x1, x2 = x2, x1
            if y1 > y2:
                y1, y2 = y2, y1
                
            return (x1, y1, x2, y2)
        except ValueError:
            return None
            
    def get_triangle_coords(self):
        """Получить координаты треугольника"""
        try:
            x0 = float(self.tri_vars['tri_x0'].get())  # прямой угол
            y0 = float(self.tri_vars['tri_y0'].get())
            x1 = float(self.tri_vars['tri_x1'].get())  # конец первого катета
            y1 = float(self.tri_vars['tri_y1'].get())  # конец второго катета
            
            # Формируем треугольник: прямой угол + два конца катетов
            return ((x0, y0), (x1, y0), (x0, y1))
        except ValueError:
            return None
    
    def calculate_and_plot(self):
        """Основной метод расчета и отображения"""
        rectangle = self.get_rectangle_coords()
        triangle = self.get_triangle_coords()
        
        if rectangle is None or triangle is None:
            self.show_error("Ошибка ввода данных!")
            return
            
        # Очищаем график
        self.ax.clear()
        self.setup_plot_appearance()
        
        # Отображаем фигуры
        self.plot_rectangle(rectangle)
        self.plot_triangle(triangle)
        
        # Расчеты
        intersect = triangle_rectangle_intersect(triangle, rectangle)
        rect_p = rectangle_perimeter(*rectangle)
        tri_p = triangle_perimeter(triangle)
        
        # Обновляем результаты
        self.update_results(rectangle, triangle, intersect, rect_p, tri_p)
        
        # Настраиваем масштаб графика
        self.adjust_plot_limits(rectangle, triangle)
        
        self.canvas.draw()
        
    def setup_plot_appearance(self):
        """Настройка внешнего вида графика"""
        self.ax.set_xlabel('X координата', fontsize=12)
        self.ax.set_ylabel('Y координата', fontsize=12)
        self.ax.grid(True, alpha=0.3, linestyle='--')
        self.ax.set_aspect('equal')
        
    def plot_rectangle(self, rectangle):
        """Отображение прямоугольника"""
        x1, y1, x2, y2 = rectangle
        width = x2 - x1
        height = y2 - y1
        
        rect = Rectangle((x1, y1), width, height, 
                        linewidth=3, edgecolor='#3498db', 
                        facecolor='#3498db', alpha=0.3,
                        label=f'Прямоугольник\nПериметр: {rectangle_perimeter(*rectangle):.2f}')
        self.ax.add_patch(rect)
        
        # Добавляем координаты углов
        corners = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
        for i, (x, y) in enumerate(corners):
            self.ax.plot(x, y, 'o', color='#2980b9', markersize=8)
            self.ax.annotate(f'({x},{y})', (x, y), xytext=(5, 5), 
                           textcoords='offset points', fontsize=8,
                           bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))
    
    def plot_triangle(self, triangle):
        """Отображение треугольника"""
        tri_array = np.array(triangle)
        
        triangle_patch = Polygon(tri_array, 
                               linewidth=3, edgecolor='#e74c3c',
                               facecolor='#e74c3c', alpha=0.3,
                               label=f'Треугольник\nПериметр: {triangle_perimeter(triangle):.2f}')
        self.ax.add_patch(triangle_patch)
        
        # Добавляем координаты вершин
        for i, (x, y) in enumerate(triangle):
            self.ax.plot(x, y, 's', color='#c0392b', markersize=8)
            labels = ['Прямой угол', '1-й катет', '2-й катет']
            self.ax.annotate(f'{labels[i]}\n({x},{y})', (x, y), xytext=(5, -15), 
                           textcoords='offset points', fontsize=8,
                           bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
    
    def adjust_plot_limits(self, rectangle, triangle):
        """Автоматическая настройка масштаба графика"""
        all_x = [rectangle[0], rectangle[2]] + [p[0] for p in triangle]
        all_y = [rectangle[1], rectangle[3]] + [p[1] for p in triangle]
        
        margin = 1
        self.ax.set_xlim(min(all_x) - margin, max(all_x) + margin)
        self.ax.set_ylim(min(all_y) - margin, max(all_y) + margin)
        
        # Добавляем легенду
        self.ax.legend(loc='upper right', bbox_to_anchor=(1, 1))
        
    def update_results(self, rectangle, triangle, intersect, rect_p, tri_p):
        """Обновление результатов расчета"""
        self.result_text.delete(1.0, tk.END)
        
        result = f"""
🔍 АНАЛИЗ ФИГУР:

📐 Прямоугольник:
   От ({rectangle[0]:.1f}, {rectangle[1]:.1f})
   До ({rectangle[2]:.1f}, {rectangle[3]:.1f})
   Размеры: {abs(rectangle[2]-rectangle[0]):.1f} × {abs(rectangle[3]-rectangle[1]):.1f}
   Периметр: {rect_p:.2f}

🔺 Треугольник:
   Вершины: {triangle[0]}, {triangle[1]}, {triangle[2]}
   Периметр: {tri_p:.2f}

🎯 РЕЗУЛЬТАТ:
   Пересекаются: {"✅ ДА" if intersect else "❌ НЕТ"}
   
   {f"🎉 Общий периметр: {rect_p + tri_p:.2f}" if intersect else "⚠️ Общий периметр не определен"}

📋 Катеты треугольника:
   • Горизонтальный: {abs(triangle[1][0] - triangle[0][0]):.2f}
   • Вертикальный: {abs(triangle[2][1] - triangle[0][1]):.2f}
   • Гипотенуза: {math.sqrt((triangle[1][0] - triangle[2][0])**2 + (triangle[1][1] - triangle[2][1])**2):.2f}
"""
        
        self.result_text.insert(1.0, result)
        
        # Устанавливаем цвет заголовка в зависимости от результата
        title_color = '#27ae60' if intersect else '#e74c3c'
        title_text = "✅ ФИГУРЫ ПЕРЕСЕКАЮТСЯ" if intersect else "❌ ФИГУРЫ НЕ ПЕРЕСЕКАЮТСЯ"
        self.ax.set_title(title_text, fontsize=14, fontweight='bold', color=title_color)
        
    def on_data_change(self, event=None):
        """Обработчик изменения данных - автоматический пересчет"""
        # Небольшая задержка для плавности
        self.root.after(500, self.calculate_and_plot)
        
    def clear_data(self):
        """Очистка всех полей"""
        defaults = {
            'rect_x1': '0', 'rect_y1': '0', 'rect_x2': '4', 'rect_y2': '3',
            'tri_x0': '1', 'tri_y0': '1', 'tri_x1': '3', 'tri_y1': '3'
        }
        
        for var_name, default in defaults.items():
            if var_name in self.rect_vars:
                self.rect_vars[var_name].set(default)
            if var_name in self.tri_vars:
                self.tri_vars[var_name].set(default)
                
        self.calculate_and_plot()
        
    def show_error(self, message):
        """Показ сообщения об ошибке"""
        messagebox.showerror("Ошибка", message)

def main():
    """Главная функция запуска GUI"""
    root = tk.Tk()
    
    # Настройка стиля
    style = ttk.Style()
    style.theme_use('clam')
    
    app = GeometryCalculatorGUI(root)
    
    # Центрирование окна
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (1200 // 2)
    y = (root.winfo_screenheight() // 2) - (800 // 2)
    root.geometry(f"1200x800+{x}+{y}")
    
    print("🚀 Запуск графического интерфейса...")
    print("💡 Измените координаты и наблюдайте результат в реальном времени!")
    
    root.mainloop()

if __name__ == "__main__":
    main() 