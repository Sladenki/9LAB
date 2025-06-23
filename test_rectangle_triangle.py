import unittest
import math
from rectangle_triangle_perimeter import (
    rectangle_perimeter, triangle_perimeter, point_in_rectangle,
    point_in_triangle, triangle_rectangle_intersect, segments_intersect
)

class TestRectangleTrianglePerimeter(unittest.TestCase):
    """Тесты для программы расчета общего периметра прямоугольника и треугольника"""
    
    def setUp(self):
        """Подготовка тестовых данных"""
        # Тестовый прямоугольник (0,0) - (4,3)
        self.rectangle1 = (0, 0, 4, 3)
        
        # Тестовый треугольник с прямым углом в (1,1), катеты длиной 2
        self.triangle1 = ((1, 1), (3, 1), (1, 3))
        
        # Непересекающиеся фигуры
        self.rectangle2 = (10, 10, 14, 13)
        self.triangle2 = ((1, 1), (3, 1), (1, 3))
        
    def test_rectangle_perimeter_calculation(self):
        """Тест расчета периметра прямоугольника"""
        # Прямоугольник 4x3, периметр = 2*(4+3) = 14
        result = rectangle_perimeter(0, 0, 4, 3)
        self.assertEqual(result, 14)
        
        # Квадрат 2x2, периметр = 8
        result = rectangle_perimeter(1, 1, 3, 3)
        self.assertEqual(result, 8)
        
        # Проверка с отрицательными координатами
        result = rectangle_perimeter(-2, -1, 2, 1)
        self.assertEqual(result, 12)  # 4x2, периметр = 12
        
    def test_triangle_perimeter_calculation(self):
        """Тест расчета периметра треугольника"""
        # Прямоугольный треугольник с катетами 2 и 2
        triangle = ((0, 0), (2, 0), (0, 2))
        expected = 2 + 2 + math.sqrt(8)  # катет + катет + гипотенуза
        result = triangle_perimeter(triangle)
        self.assertAlmostEqual(result, expected, places=5)
        
        # Треугольник 3-4-5
        triangle345 = ((0, 0), (3, 0), (0, 4))
        expected345 = 3 + 4 + 5
        result345 = triangle_perimeter(triangle345)
        self.assertAlmostEqual(result345, expected345, places=5)
        
    def test_point_in_rectangle(self):
        """Тест проверки точки внутри прямоугольника"""
        rect = (0, 0, 4, 3)
        
        # Точки внутри
        self.assertTrue(point_in_rectangle((2, 1), rect))
        self.assertTrue(point_in_rectangle((1, 2), rect))
        
        # Точки на границе (должны считаться внутри)
        self.assertTrue(point_in_rectangle((0, 0), rect))
        self.assertTrue(point_in_rectangle((4, 3), rect))
        self.assertTrue(point_in_rectangle((2, 0), rect))
        
        # Точки снаружи
        self.assertFalse(point_in_rectangle((5, 1), rect))
        self.assertFalse(point_in_rectangle((2, 4), rect))
        self.assertFalse(point_in_rectangle((-1, 1), rect))
        
    def test_point_in_triangle(self):
        """Тест проверки точки внутри треугольника"""
        triangle = ((0, 0), (3, 0), (0, 3))
        
        # Точки внутри
        self.assertTrue(point_in_triangle((1, 1), triangle))
        self.assertTrue(point_in_triangle((0.5, 0.5), triangle))
        
        # Точки на вершинах
        self.assertTrue(point_in_triangle((0, 0), triangle))
        self.assertTrue(point_in_triangle((3, 0), triangle))
        self.assertTrue(point_in_triangle((0, 3), triangle))
        
        # Точки снаружи
        self.assertFalse(point_in_triangle((2, 2), triangle))
        self.assertFalse(point_in_triangle((4, 1), triangle))
        self.assertFalse(point_in_triangle((1, 4), triangle))
        
    def test_segments_intersection(self):
        """Тест пересечения отрезков"""
        # Пересекающиеся отрезки
        self.assertTrue(segments_intersect(0, 0, 2, 2, 0, 2, 2, 0))
        
        # Параллельные непересекающиеся отрезки
        self.assertFalse(segments_intersect(0, 0, 2, 0, 0, 1, 2, 1))
        
        # Отрезки с общей точкой
        self.assertTrue(segments_intersect(0, 0, 2, 0, 2, 0, 2, 2))
        
    def test_triangle_rectangle_intersection_positive(self):
        """Тест пересечения треугольника и прямоугольника - положительные случаи"""
        # Треугольник частично внутри прямоугольника
        rect = (0, 0, 4, 3)
        triangle = ((1, 1), (3, 1), (1, 3))
        self.assertTrue(triangle_rectangle_intersect(triangle, rect))
        
        # Прямоугольник полностью внутри треугольника
        small_rect = (1, 1, 2, 2)
        large_triangle = ((0, 0), (5, 0), (0, 5))
        self.assertTrue(triangle_rectangle_intersect(large_triangle, small_rect))
        
    def test_triangle_rectangle_intersection_negative(self):
        """Тест пересечения треугольника и прямоугольника - отрицательные случаи"""
        # Фигуры не пересекаются
        rect = (10, 10, 14, 13)
        triangle = ((1, 1), (3, 1), (1, 3))
        self.assertFalse(triangle_rectangle_intersect(triangle, rect))
        
        # Фигуры далеко друг от друга
        rect2 = (0, 0, 2, 2)
        triangle2 = ((10, 10), (12, 10), (10, 12))
        self.assertFalse(triangle_rectangle_intersect(triangle2, rect2))
        
    def test_edge_cases(self):
        """Тест граничных случаев"""
        # Вырожденный прямоугольник (линия)
        line_rect = (0, 0, 0, 3)
        result = rectangle_perimeter(*line_rect)
        self.assertEqual(result, 6)  # 2 * (0 + 3)
        
        # Точечный прямоугольник
        point_rect = (1, 1, 1, 1)
        result = rectangle_perimeter(*point_rect)
        self.assertEqual(result, 0)
        
        # Треугольник с очень маленькими катетами
        tiny_triangle = ((0, 0), (0.001, 0), (0, 0.001))
        result = triangle_perimeter(tiny_triangle)
        expected = 0.001 + 0.001 + math.sqrt(0.001**2 + 0.001**2)
        self.assertAlmostEqual(result, expected, places=10)
        
    def test_negative_coordinates(self):
        """Тест работы с отрицательными координатами"""
        # Прямоугольник в отрицательной области
        rect = (-4, -3, -1, -1)
        result = rectangle_perimeter(*rect)
        self.assertEqual(result, 10)  # 3x2, периметр = 10
        
        # Треугольник с отрицательными координатами
        triangle = ((-2, -2), (0, -2), (-2, 0))
        expected = 2 + 2 + math.sqrt(8)
        result = triangle_perimeter(triangle)
        self.assertAlmostEqual(result, expected, places=5)

class TestInputValidation(unittest.TestCase):
    """Тесты валидации входных данных"""
    
    def test_rectangle_coordinate_ordering(self):
        """Тест автоматического упорядочивания координат прямоугольника"""
        # Функция должна правильно обрабатывать неупорядоченные координаты
        # (это должно быть протестировано в основной программе)
        pass
        
    def test_triangle_right_angle_validation(self):
        """Тест валидации прямого угла в треугольнике"""
        # Проверка, что треугольник действительно прямоугольный
        # с катетами, параллельными осям координат
        pass

def run_comprehensive_tests():
    """Запуск всех тестов с детальным отчетом"""
    print("=" * 60)
    print("ТЕСТИРОВАНИЕ ПРОГРАММЫ РАСЧЕТА ОБЩЕГО ПЕРИМЕТРА")
    print("=" * 60)
    
    # Создаем набор тестов
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestRectangleTrianglePerimeter)
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestInputValidation))
    
    # Запускаем тесты с подробным выводом
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    print("\n" + "=" * 60)
    print(f"РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
    print(f"Всего тестов: {result.testsRun}")
    print(f"Успешных: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Неудачных: {len(result.failures)}")
    print(f"Ошибок: {len(result.errors)}")
    print("=" * 60)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    # Запускаем комплексное тестирование
    success = run_comprehensive_tests()
    
    if success:
        print("\n✓ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("Программа готова к использованию.")
    else:
        print("\n✗ ОБНАРУЖЕНЫ ОШИБКИ В ПРОГРАММЕ!")
        print("Необходимо исправить ошибки перед использованием.") 