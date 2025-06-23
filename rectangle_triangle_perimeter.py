import math

def input_rectangle():
    """Ввод координат прямоугольника"""
    print("Введите координаты прямоугольника:")
    x1 = float(input("x1 (левый нижний угол): "))
    y1 = float(input("y1 (левый нижний угол): "))
    x2 = float(input("x2 (правый верхний угол): "))
    y2 = float(input("y2 (правый верхний угол): "))
    
    # Убеждаемся, что координаты правильно упорядочены
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1
    
    return (x1, y1, x2, y2)

def input_triangle():
    """Ввод координат прямоугольного треугольника с катетами параллельными осям координат"""
    print("\nВведите координаты прямоугольного треугольника:")
    print("(катеты параллельны осям координат)")
    
    # Вершина прямого угла
    x_right = float(input("x координата вершины прямого угла: "))
    y_right = float(input("y координата вершины прямого угла: "))
    
    # Вершины на концах катетов
    x_end1 = float(input("x координата конца первого катета: "))
    y_end1 = y_right  # первый катет параллелен оси X
    
    x_end2 = x_right  # второй катет параллелен оси Y
    y_end2 = float(input("y координата конца второго катета: "))
    
    return ((x_right, y_right), (x_end1, y_end1), (x_end2, y_end2))

def rectangle_perimeter(x1, y1, x2, y2):
    """Вычисление периметра прямоугольника"""
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    return 2 * (width + height)

def triangle_perimeter(triangle):
    """Вычисление периметра треугольника"""
    p1, p2, p3 = triangle
    
    # Стороны треугольника
    side1 = abs(p2[0] - p1[0])  # катет 1
    side2 = abs(p3[1] - p1[1])  # катет 2
    side3 = math.sqrt((p2[0] - p3[0])**2 + (p2[1] - p3[1])**2)  # гипотенуза
    
    return side1 + side2 + side3

def point_in_rectangle(point, rect):
    """Проверка, находится ли точка внутри прямоугольника"""
    x, y = point
    x1, y1, x2, y2 = rect
    return x1 <= x <= x2 and y1 <= y <= y2

def segments_intersect(x1, y1, x2, y2, x3, y3, x4, y4):
    """Проверка пересечения двух отрезков"""
    # Проверяем, пересекаются ли отрезки (x1,y1)-(x2,y2) и (x3,y3)-(x4,y4)
    
    def ccw(A, B, C):
        return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])
    
    A, B, C, D = (x1, y1), (x2, y2), (x3, y3), (x4, y4)
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

def triangle_rectangle_intersect(triangle, rectangle):
    """Проверка пересечения треугольника и прямоугольника"""
    tri_p1, tri_p2, tri_p3 = triangle
    rect_x1, rect_y1, rect_x2, rect_y2 = rectangle
    
    # Вершины прямоугольника
    rect_corners = [
        (rect_x1, rect_y1), (rect_x2, rect_y1),
        (rect_x2, rect_y2), (rect_x1, rect_y2)
    ]
    
    # Проверяем, находятся ли вершины треугольника внутри прямоугольника
    for point in triangle:
        if point_in_rectangle(point, rectangle):
            return True
    
    # Проверяем, находятся ли вершины прямоугольника внутри треугольника
    for corner in rect_corners:
        if point_in_triangle(corner, triangle):
            return True
    
    # Проверяем пересечение сторон треугольника со сторонами прямоугольника
    triangle_sides = [
        (tri_p1, tri_p2), (tri_p2, tri_p3), (tri_p3, tri_p1)
    ]
    
    rectangle_sides = [
        ((rect_x1, rect_y1), (rect_x2, rect_y1)),  # нижняя сторона
        ((rect_x2, rect_y1), (rect_x2, rect_y2)),  # правая сторона
        ((rect_x2, rect_y2), (rect_x1, rect_y2)),  # верхняя сторона
        ((rect_x1, rect_y2), (rect_x1, rect_y1))   # левая сторона
    ]
    
    for tri_side in triangle_sides:
        for rect_side in rectangle_sides:
            if segments_intersect(
                tri_side[0][0], tri_side[0][1], tri_side[1][0], tri_side[1][1],
                rect_side[0][0], rect_side[0][1], rect_side[1][0], rect_side[1][1]
            ):
                return True
    
    return False

def point_in_triangle(point, triangle):
    """Проверка, находится ли точка внутри треугольника"""
    x, y = point
    x1, y1 = triangle[0]
    x2, y2 = triangle[1]
    x3, y3 = triangle[2]
    
    # Используем барицентрические координаты
    denom = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
    if abs(denom) < 1e-10:
        return False
    
    a = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / denom
    b = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / denom
    c = 1 - a - b
    
    return 0 <= a <= 1 and 0 <= b <= 1 and 0 <= c <= 1

def calculate_combined_perimeter(rectangle, triangle):
    """Вычисление общего периметра пересекающихся фигур"""
    rect_perimeter = rectangle_perimeter(*rectangle)
    tri_perimeter = triangle_perimeter(triangle)
    
    if not triangle_rectangle_intersect(triangle, rectangle):
        return 0, rect_perimeter, tri_perimeter, "Фигуры не пересекаются"
    
    # Упрощенная модель: общий периметр = сумма периметров минус пересекающиеся участки
    # Для точного решения нужен сложный алгоритм вычисления контура объединения
    
    # Примерная оценка длины пересекающихся границ
    intersection_length = estimate_intersection_boundary_length(rectangle, triangle)
    
    # Общий периметр = периметр объединения
    combined_perimeter = rect_perimeter + tri_perimeter - 2 * intersection_length
    
    details = {
        'rect_perimeter': rect_perimeter,
        'tri_perimeter': tri_perimeter,
        'intersection_length': intersection_length,
        'combined_perimeter': max(combined_perimeter, max(rect_perimeter, tri_perimeter))
    }
    
    print(f"Периметр прямоугольника: {rect_perimeter:.2f}")
    print(f"Периметр треугольника: {tri_perimeter:.2f}")
    print(f"Длина пересекающихся границ: {intersection_length:.2f}")
    print(f"Общий периметр объединенной фигуры: {details['combined_perimeter']:.2f}")
    
    return details['combined_perimeter'], rect_perimeter, tri_perimeter, "Пересекаются"

def estimate_intersection_boundary_length(rectangle, triangle):
    """Примерная оценка длины пересекающихся границ"""
    x1, y1, x2, y2 = rectangle
    tri_p1, tri_p2, tri_p3 = triangle
    
    # Стороны прямоугольника
    rect_sides = [
        ((x1, y1), (x2, y1)),  # нижняя
        ((x2, y1), (x2, y2)),  # правая
        ((x2, y2), (x1, y2)),  # верхняя
        ((x1, y2), (x1, y1))   # левая
    ]
    
    # Стороны треугольника
    tri_sides = [
        (tri_p1, tri_p2),
        (tri_p2, tri_p3),
        (tri_p3, tri_p1)
    ]
    
    total_intersection_length = 0.0
    
    # Находим пересечения сторон
    for rect_side in rect_sides:
        for tri_side in tri_sides:
            intersection_segment = find_segment_intersection(rect_side, tri_side)
            if intersection_segment:
                length = segment_length(intersection_segment)
                total_intersection_length += length
    
    return total_intersection_length

def find_segment_intersection(seg1, seg2):
    """Находит пересечение двух отрезков, возвращает отрезок пересечения или None"""
    (x1, y1), (x2, y2) = seg1
    (x3, y3), (x4, y4) = seg2
    
    # Проверяем параллельность
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(denom) < 1e-10:
        return None
    
    # Находим точку пересечения прямых
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom
    
    # Проверяем, что пересечение происходит в пределах отрезков
    if 0 <= t <= 1 and 0 <= u <= 1:
        ix = x1 + t * (x2 - x1)
        iy = y1 + t * (y2 - y1)
        return ((ix, iy), (ix, iy))  # Точечное пересечение
    
    return None

def segment_length(segment):
    """Вычисляет длину отрезка"""
    if segment is None:
        return 0
    (x1, y1), (x2, y2) = segment
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def main():
    """Основная функция программы"""
    print("=== ПРОГРАММА РАСЧЕТА ОБЩЕГО ПЕРИМЕТРА ===")
    print("Задача: определить общую длину периметра пересекающихся")
    print("прямоугольника и прямоугольного треугольника")
    print("=" * 50)
    
    # Ввод данных
    rectangle = input_rectangle()
    triangle = input_triangle()
    
    # Проверка пересечения и расчет общего периметра
    if triangle_rectangle_intersect(triangle, rectangle):
        print("\n✓ Фигуры пересекаются или соприкасаются!")
        print("Вычисляем общий периметр объединенной фигуры...")
        
        result = calculate_combined_perimeter(rectangle, triangle)
        if len(result) == 4:
            combined_p, rect_p, tri_p, status = result
            print(f"\n=== РЕЗУЛЬТАТЫ РАСЧЕТА ===")
            print(f"Периметр прямоугольника: {rect_p:.2f}")
            print(f"Периметр треугольника: {tri_p:.2f}")
            print(f"Общий периметр объединенной фигуры: {combined_p:.2f}")
        else:
            combined_perimeter = result
            print(f"\nОбщая длина периметра: {combined_perimeter:.2f}")
        
    else:
        print("\n✗ Фигуры не пересекаются и не соприкасаются!")
        print("Общий периметр не определен.")

if __name__ == "__main__":
    main() 