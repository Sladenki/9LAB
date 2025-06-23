#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестирование всех ветвей потока управления для лабораторной работы №9
Требования: поле 600x600, координаты от -200 до 200, центр в центре
"""

import unittest
import sys
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Добавляем текущую директорию в путь для импорта модулей
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rectangle_triangle_perimeter import (
    rectangle_perimeter, triangle_perimeter,
    triangle_rectangle_intersect, point_in_rectangle,
    point_in_triangle, segments_intersect
)

class TestAllBranches(unittest.TestCase):
    """Тестирование всех ветвей графа потока управления"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.test_counter = 0
        
    def create_test_visualization(self, rectangle, triangle, test_name, intersects, test_num):
        """Создание графической иллюстрации для теста 600x600"""
        # Создаем фигуру строго 600x600 пикселей
        fig, ax = plt.subplots(figsize=(6, 6), dpi=100)
        fig.patch.set_facecolor('white')
        
        # Настройка осей согласно требованиям: -200 до 200, центр в центре
        ax.set_xlim(-200, 200)
        ax.set_ylim(-200, 200)
        ax.set_xlabel('X координата', fontsize=10)
        ax.set_ylabel('Y координата', fontsize=10)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_aspect('equal')
        
        # Оси через центр
        ax.axhline(y=0, color='black', linewidth=0.8, alpha=0.8)
        ax.axvline(x=0, color='black', linewidth=0.8, alpha=0.8)
        
        # Градация каждые 50 единиц
        major_ticks = np.arange(-200, 201, 50)
        ax.set_xticks(major_ticks)
        ax.set_yticks(major_ticks)
        
        # Отображение прямоугольника
        x1, y1, x2, y2 = rectangle
        width = x2 - x1
        height = y2 - y1
        rect_color = '#3498db' if intersects else '#95a5a6'
        rect = patches.Rectangle((x1, y1), width, height,
                               linewidth=2, edgecolor=rect_color,
                               facecolor=rect_color, alpha=0.4,
                               label=f'Прямоугольник {width:.1f}×{height:.1f}')
        ax.add_patch(rect)
        
        # Отображение треугольника
        tri_color = '#e67e22' if intersects else '#95a5a6'
        tri_array = np.array(triangle)
        triangle_patch = patches.Polygon(tri_array,
                                       linewidth=2, edgecolor=tri_color,
                                       facecolor=tri_color, alpha=0.4,
                                       label='Треугольник')
        ax.add_patch(triangle_patch)
        
        # Точки вершин
        corners = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
        for x, y in corners:
            ax.plot(x, y, 'o', color='#2980b9', markersize=4)
        
        for x, y in triangle:
            ax.plot(x, y, 's', color='#d35400', markersize=4)
        
        # Заголовок и легенда
        status = "ПЕРЕСЕКАЮТСЯ" if intersects else "НЕ ПЕРЕСЕКАЮТСЯ"
        color = '#27ae60' if intersects else '#e74c3c'
        ax.set_title(f"ТЕСТ {test_num}: {test_name}\n{status}",
                    fontsize=11, fontweight='bold', color=color)
        ax.legend(loc='upper right', fontsize=9)
        
        # Сохранение графика
        filename = f"test_{test_num:02d}_{test_name.replace(' ', '_').replace(':', '')}.png"
        plt.tight_layout()
        plt.savefig(filename, dpi=100, bbox_inches='tight')
        plt.close()
        
        print(f"📊 График сохранен: {filename}")
        return filename
    
    def test_01_intersecting_standard(self):
        """ВЕТВЬ 1: Стандартное пересечение фигур"""
        rectangle = (-50, -30, 50, 30)
        triangle = ((-25, -15), (25, -15), (-25, 15))
        
        result = triangle_rectangle_intersect(triangle, rectangle)
        
        self.assertTrue(result, "Фигуры должны пересекаться")
        
        # Графическая иллюстрация
        self.create_test_visualization(rectangle, triangle, 
                                     "Стандартное пересечение", result, 1)
        
        print("✅ ТЕСТ 1: Стандартное пересечение - ПРОЙДЕН")
    
    def test_02_no_intersection_far_apart(self):
        """ВЕТВЬ 2: Фигуры не пересекаются - далеко друг от друга"""
        rectangle = (-100, -50, -20, 20)
        triangle = ((50, 30), (80, 30), (50, 60))
        
        result = triangle_rectangle_intersect(triangle, rectangle)
        
        self.assertFalse(result, "Фигуры не должны пересекаться")
        
        # Графическая иллюстрация
        self.create_test_visualization(rectangle, triangle,
                                     "Далеко друг от друга", result, 2)
        
        print("✅ ТЕСТ 2: Фигуры далеко - ПРОЙДЕН")
    
    def test_03_touching_boundary(self):
        """ВЕТВЬ 3: Граничный случай - фигуры касаются"""
        rectangle = (-60, -40, 0, 40)
        triangle = ((0, -20), (40, -20), (0, 20))
        
        result = triangle_rectangle_intersect(triangle, rectangle)
        
        self.assertTrue(result, "Касающиеся фигуры должны считаться пересекающимися")
        
        # Графическая иллюстрация
        self.create_test_visualization(rectangle, triangle,
                                     "Граничное касание", result, 3)
        
        print("✅ ТЕСТ 3: Граничное касание - ПРОЙДЕН")
    
    def test_04_boundary_values_max_range(self):
        """ВЕТВЬ 4: Граничные значения - максимальный диапазон поля"""
        rectangle = (-200, -200, -100, -100)
        triangle = ((100, 100), (200, 100), (100, 200))
        
        # Проверяем, что координаты в допустимых границах
        all_coords = [-200, -200, -100, -100, 100, 100, 200, 100, 100, 200]
        for coord in all_coords:
            self.assertTrue(-200 <= coord <= 200, f"Координата {coord} вне границ поля")
        
        result = triangle_rectangle_intersect(triangle, rectangle)
        
        self.assertFalse(result, "Фигуры на границах не должны пересекаться")
        
        # Графическая иллюстрация
        self.create_test_visualization(rectangle, triangle,
                                     "Границы поля", result, 4)
        
        print("✅ ТЕСТ 4: Граничные значения - ПРОЙДЕН")
    
    def test_05_zero_coordinates_center(self):
        """ВЕТВЬ 5: Нулевые координаты - центр системы координат"""
        rectangle = (-20, -20, 20, 20)
        triangle = ((0, 0), (30, 0), (0, 30))
        
        result = triangle_rectangle_intersect(triangle, rectangle)
        
        self.assertTrue(result, "Фигуры через центр должны пересекаться")
        
        # Графическая иллюстрация
        self.create_test_visualization(rectangle, triangle,
                                     "Через центр координат", result, 5)
        
        print("✅ ТЕСТ 5: Центр координат - ПРОЙДЕН")
    
    def test_06_triangle_inside_rectangle(self):
        """ВЕТВЬ 6: Треугольник полностью внутри прямоугольника"""
        rectangle = (-80, -80, 80, 80)
        triangle = ((-20, -20), (20, -20), (-20, 20))
        
        result = triangle_rectangle_intersect(triangle, rectangle)
        
        self.assertTrue(result, "Треугольник внутри прямоугольника должен пересекаться")
        
        # Дополнительная проверка: все вершины треугольника внутри прямоугольника
        for point in triangle:
            self.assertTrue(point_in_rectangle(point, rectangle),
                          f"Точка {point} должна быть внутри прямоугольника")
        
        # Графическая иллюстрация
        self.create_test_visualization(rectangle, triangle,
                                     "Треугольник внутри", result, 6)
        
        print("✅ ТЕСТ 6: Треугольник внутри - ПРОЙДЕН")
    
    def test_07_rectangle_inside_triangle(self):
        """ВЕТВЬ 7: Прямоугольник полностью внутри треугольника"""
        rectangle = (-10, -10, 10, 10)
        triangle = ((-50, -50), (50, -50), (-50, 50))
        
        result = triangle_rectangle_intersect(triangle, rectangle)
        
        self.assertTrue(result, "Прямоугольник внутри треугольника должен пересекаться")
        
        # Дополнительная проверка: все углы прямоугольника внутри треугольника
        corners = [(-10, -10), (10, -10), (10, 10), (-10, 10)]
        for corner in corners:
            self.assertTrue(point_in_triangle(corner, triangle),
                          f"Угол {corner} должен быть внутри треугольника")
        
        # Графическая иллюстрация
        self.create_test_visualization(rectangle, triangle,
                                     "Прямоугольник внутри", result, 7)
        
        print("✅ ТЕСТ 7: Прямоугольник внутри - ПРОЙДЕН")
    
    def test_08_degenerate_line_rectangle(self):
        """ВЕТВЬ 8: Вырожденный случай - прямоугольник как линия"""
        rectangle = (0, -30, 0, 30)  # Вырожденный в линию
        triangle = ((-20, -10), (20, -10), (-20, 10))
        
        result = triangle_rectangle_intersect(triangle, rectangle)
        
        # Проверяем, что алгоритм корректно обрабатывает вырожденный случай
        self.assertTrue(result, "Линия должна пересекаться с треугольником")
        
        # Графическая иллюстрация
        self.create_test_visualization(rectangle, triangle,
                                     "Вырожденная линия", result, 8)
        
        print("✅ ТЕСТ 8: Вырожденный случай - ПРОЙДЕН")
    
    def test_09_edge_intersection_only(self):
        """ВЕТВЬ 9: Пересечение только по ребрам"""
        rectangle = (-40, -40, 40, -20)
        triangle = ((-30, -20), (30, -20), (-30, 0))
        
        result = triangle_rectangle_intersect(triangle, rectangle)
        
        self.assertTrue(result, "Пересечение по ребру должно детектироваться")
        
        # Графическая иллюстрация
        self.create_test_visualization(rectangle, triangle,
                                     "Пересечение ребер", result, 9)
        
        print("✅ ТЕСТ 9: Пересечение ребер - ПРОЙДЕН")
    
    def test_10_negative_coordinates_boundary(self):
        """ВЕТВЬ 10: Отрицательные координаты на границе"""
        rectangle = (-200, -200, -150, -150)
        triangle = ((-175, -175), (-125, -175), (-175, -125))
        
        result = triangle_rectangle_intersect(triangle, rectangle)
        
        self.assertTrue(result, "Пересечение в отрицательной области должно работать")
        
        # Проверяем граничные значения
        self.assertEqual(rectangle[0], -200, "Левая граница должна быть -200")
        self.assertEqual(rectangle[1], -200, "Нижняя граница должна быть -200")
        
        # Графическая иллюстрация
        self.create_test_visualization(rectangle, triangle,
                                     "Отрицательные границы", result, 10)
        
        print("✅ ТЕСТ 10: Отрицательные границы - ПРОЙДЕН")
    
    def test_11_perimeter_calculations(self):
        """ВЕТВЬ 11: Проверка расчета периметров"""
        rectangle = (-30, -20, 30, 20)
        triangle = ((-15, -10), (15, -10), (-15, 10))
        
        # Проверяем расчет периметра прямоугольника
        rect_p = rectangle_perimeter(*rectangle)
        expected_rect_p = 2 * (60 + 40)  # 2 * (ширина + высота)
        self.assertEqual(rect_p, expected_rect_p, "Периметр прямоугольника неверен")
        
        # Проверяем расчет периметра треугольника
        tri_p = triangle_perimeter(triangle)
        # Катеты: 30 и 20, гипотенуза: sqrt(30² + 20²) ≈ 36.06
        expected_tri_p = 30 + 20 + (30**2 + 20**2)**0.5
        self.assertAlmostEqual(tri_p, expected_tri_p, places=2, 
                              msg="Периметр треугольника неверен")
        
        # Графическая иллюстрация
        result = triangle_rectangle_intersect(triangle, rectangle)
        self.create_test_visualization(rectangle, triangle,
                                     "Расчет периметров", result, 11)
        
        print(f"✅ ТЕСТ 11: Периметры - прямоугольник: {rect_p}, треугольник: {tri_p:.2f}")
    
    def test_12_segments_intersection_logic(self):
        """ВЕТВЬ 12: Проверка логики пересечения отрезков"""
        # Тестируем функцию segments_intersect
        
        # Пересекающиеся отрезки
        self.assertTrue(segments_intersect(0, 0, 10, 10, 5, 0, 5, 10),
                       "Пересекающиеся отрезки не детектированы")
        
        # Не пересекающиеся отрезки
        self.assertFalse(segments_intersect(0, 0, 5, 5, 10, 10, 15, 15),
                        "Непересекающиеся отрезки детектированы как пересекающиеся")
        
        # Параллельные отрезки
        self.assertFalse(segments_intersect(0, 0, 10, 0, 0, 5, 10, 5),
                        "Параллельные отрезки детектированы как пересекающиеся")
        
        print("✅ ТЕСТ 12: Логика пересечения отрезков - ПРОЙДЕН")
    
    def test_13_point_in_shapes_logic(self):
        """ВЕТВЬ 13: Проверка принадлежности точки фигурам"""
        rectangle = (-50, -50, 50, 50)
        triangle = ((-30, -30), (30, -30), (-30, 30))
        
        # Точки внутри прямоугольника
        self.assertTrue(point_in_rectangle((0, 0), rectangle),
                       "Центр должен быть внутри прямоугольника")
        self.assertFalse(point_in_rectangle((60, 60), rectangle),
                        "Точка вне прямоугольника детектирована как внутри")
        
        # Точки внутри треугольника
        self.assertTrue(point_in_triangle((-20, -20), triangle),
                       "Точка должна быть внутри треугольника")
        self.assertFalse(point_in_triangle((20, 20), triangle),
                        "Точка вне треугольника детектирована как внутри")
        
        print("✅ ТЕСТ 13: Принадлежность точки - ПРОЙДЕН")
    
    def run_all_branch_tests(self):
        """Запуск всех тестов для покрытия ветвей"""
        print("\n" + "="*60)
        print("🧪 ТЕСТИРОВАНИЕ ВСЕХ ВЕТВЕЙ ПОТОКА УПРАВЛЕНИЯ")
        print("📏 Поле: 600×600 пикселей")
        print("📍 Координаты: от -200 до 200")
        print("📊 Центр: в центре поля")
        print("="*60)
        
        # Запускаем все тесты
        test_methods = [method for method in dir(self) if method.startswith('test_')]
        
        passed = 0
        failed = 0
        
        for test_method in sorted(test_methods):
            try:
                print(f"\n🔍 Выполняется: {test_method}")
                getattr(self, test_method)()
                passed += 1
            except Exception as e:
                print(f"❌ ОШИБКА в {test_method}: {e}")
                failed += 1
        
        print(f"\n" + "="*60)
        print(f"📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
        print(f"   ✅ Пройдено: {passed}")
        print(f"   ❌ Провалено: {failed}")
        print(f"   📈 Успешность: {passed/(passed+failed)*100:.1f}%")
        print("="*60)
        
        return passed, failed

def main():
    """Главная функция для запуска тестов"""
    tester = TestAllBranches()
    tester.run_all_branch_tests()

if __name__ == "__main__":
    main() 