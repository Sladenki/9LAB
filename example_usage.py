"""
Пример использования программы расчета общего периметра
для лабораторной работы по тестированию ПО
"""

from rectangle_triangle_perimeter import (
    rectangle_perimeter, triangle_perimeter, 
    triangle_rectangle_intersect, calculate_combined_perimeter
)

def example_1_intersecting_figures():
    """Пример 1: Пересекающиеся фигуры"""
    print("ПРИМЕР 1: Пересекающиеся фигуры")
    print("-" * 40)
    
    # Прямоугольник от (0,0) до (4,3)
    rectangle = (0, 0, 4, 3)
    print(f"Прямоугольник: от ({rectangle[0]},{rectangle[1]}) до ({rectangle[2]},{rectangle[3]})")
    
    # Треугольник с прямым углом в (1,1), катеты до (3,1) и (1,3)
    triangle = ((1, 1), (3, 1), (1, 3))
    print(f"Треугольник: вершины {triangle[0]}, {triangle[1]}, {triangle[2]}")
    
    # Проверка пересечения
    intersect = triangle_rectangle_intersect(triangle, rectangle)
    print(f"Пересекаются: {'Да' if intersect else 'Нет'}")
    
    if intersect:
        rect_p = rectangle_perimeter(*rectangle)
        tri_p = triangle_perimeter(triangle)
        total_p = rect_p + tri_p
        
        print(f"Периметр прямоугольника: {rect_p:.2f}")
        print(f"Периметр треугольника: {tri_p:.2f}")
        print(f"Общий периметр: {total_p:.2f}")
    
    print()

def example_2_non_intersecting_figures():
    """Пример 2: Непересекающиеся фигуры"""
    print("ПРИМЕР 2: Непересекающиеся фигуры")
    print("-" * 40)
    
    # Прямоугольник далеко от треугольника
    rectangle = (10, 10, 14, 13)
    print(f"Прямоугольник: от ({rectangle[0]},{rectangle[1]}) до ({rectangle[2]},{rectangle[3]})")
    
    # Треугольник в начале координат
    triangle = ((0, 0), (2, 0), (0, 2))
    print(f"Треугольник: вершины {triangle[0]}, {triangle[1]}, {triangle[2]}")
    
    # Проверка пересечения
    intersect = triangle_rectangle_intersect(triangle, rectangle)
    print(f"Пересекаются: {'Да' if intersect else 'Нет'}")
    
    if not intersect:
        print("Общий периметр не определен (фигуры не пересекаются)")
    
    print()

def example_3_edge_case_touching():
    """Пример 3: Соприкасающиеся фигуры"""
    print("ПРИМЕР 3: Соприкасающиеся фигуры")
    print("-" * 40)
    
    # Прямоугольник
    rectangle = (0, 0, 3, 2)
    print(f"Прямоугольник: от ({rectangle[0]},{rectangle[1]}) до ({rectangle[2]},{rectangle[3]})")
    
    # Треугольник, соприкасающийся с прямоугольником
    triangle = ((3, 0), (5, 0), (3, 2))
    print(f"Треугольник: вершины {triangle[0]}, {triangle[1]}, {triangle[2]}")
    
    # Проверка пересечения
    intersect = triangle_rectangle_intersect(triangle, rectangle)
    print(f"Пересекаются или соприкасаются: {'Да' if intersect else 'Нет'}")
    
    if intersect:
        rect_p = rectangle_perimeter(*rectangle)
        tri_p = triangle_perimeter(triangle)
        total_p = rect_p + tri_p
        
        print(f"Периметр прямоугольника: {rect_p:.2f}")
        print(f"Периметр треугольника: {tri_p:.2f}")
        print(f"Общий периметр: {total_p:.2f}")
    
    print()

def run_all_examples():
    """Запуск всех примеров"""
    print("=" * 50)
    print("ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ ПРОГРАММЫ")
    print("Лабораторная работа: Тестирование ПО")
    print("Задача: Расчет общего периметра")
    print("=" * 50)
    print()
    
    example_1_intersecting_figures()
    example_2_non_intersecting_figures()
    example_3_edge_case_touching()
    
    print("=" * 50)
    print("Примеры завершены.")
    print("Для интерактивного ввода запустите: python rectangle_triangle_perimeter.py")
    print("=" * 50)

if __name__ == "__main__":
    run_all_examples() 