import ast

class CodeGenerator(ast.NodeVisitor):
    def __init__(self):
        # Инициализация списка для хранения сгенерированного кода
        self.generated_code = []

    def generate_code(self, data):
        # Обход всех элементов входных данных и генерация соответствующего кода
        for element in data:
            self.visit(element)
        # Возвращаем сгенерированный код как строку
        return '\n'.join(self.generated_code)

    def visit(self, node):
        # Определяем имя метода для обработки данного типа узла
        method_name = f'visit_{node["class"]}'
        if hasattr(self, method_name):
            # Вызываем метод для обработки данного типа узла
            getattr(self, method_name)(node)
        else:
            # Выбрасываем исключение, если метод для данного типа узла не реализован
            raise NotImplementedError(f"Method {method_name} not implemented")

    def visit_Variable(self, node):
        # Добавляем значение переменной в сгенерированный код
        self.generated_code.append(node['value'])

    def visit_Function(self, node):
        # Генерируем заголовок функции
        self.generated_code.append(f"def {node['name']}({', '.join(node['args'])}):")
        # Увеличиваем отступ для тела функции
        self.indent()
        for i, line in enumerate(node['body']):
            # Добавляем каждую строку тела функции с отступом
            self.generated_code.append(f"    {line}")
        # Уменьшаем отступ после окончания тела функции
        self.dedent()

    def visit_Class(self, node):
        # Генерируем заголовок класса
        self.generated_code.append(f"class {node['name']}({', '.join(node['bases'])}):")
        # Увеличиваем отступ для тела класса
        self.indent()
        for i, line in enumerate(node['body']):
            # Добавляем каждую строку тела класса с отступом
            self.generated_code.append(f"    {line}")
        # Уменьшаем отступ после окончания тела класса
        self.dedent()

    def visit_Import(self, node):
        # Генерируем строку импорта модулей
        self.generated_code.append(f"import {', '.join(node['modules'])}")

    def visit_ImportFrom(self, node):
        # Генерируем строку импорта из конкретного модуля
        self.generated_code.append(f"from {node['module']} import {', '.join(node['names'])}")

    def visit_FunctionCall(self, node):
        # Генерируем строку вызова функции с аргументами
        args = ', '.join(node['args'])
        self.generated_code.append(f"{node['name']}({args})")

    def visit_Comparison(self, node):
        # Генерируем строку сравнения
        self.generated_code.append(f"{node['left']} {node['operator']} {node['right']}")

    def visit_WhileLoop(self, node):
        # Генерируем заголовок цикла while
        self.generated_code.append(f"while {node['condition']}:")
        # Увеличиваем отступ для тела цикла
        self.indent()
        for i, line in enumerate(node['body']):
            # Добавляем каждую строку тела цикла с отступом
            self.generated_code.append(f"    {line}")
        # Уменьшаем отступ после окончания тела цикла
        self.dedent()

    def visit_Conditional(self, node):
        # Генерируем заголовок условного оператора if
        self.generated_code.append(f"if {node['condition']}:")
        # Увеличиваем отступ для тела условного оператора
        self.indent()
        for line in node['body']:
            self.generated_code.append(f"    {line}")
        # Обрабатываем elif блок, если он существует
        if 'elif_condition' in node:
            self.generated_code.append(f"elif {node['elif_condition']}:")
            self.indent()
            for line in node['elif_body']:
                self.generated_code.append(f"    {line}")
            self.dedent()
        # Обрабатываем else блок, если он существует
        if 'else_body' in node:
            self.generated_code.append("else:")
            self.indent()
            for line in node['else_body']:
                self.generated_code.append(f"    {line}")
            self.dedent()

    def indent(self):
        # Увеличиваем уровень отступа
        self.generated_code.append("    ")

    def dedent(self):
        # Уменьшаем уровень отступа
        self.generated_code.pop()


# Новые входные данные
input_data = [
    {
        "class": "Function",
        "name": "test",
        "args": ["a", "b"],
        "body": [
            "print(a)",
            "print(b)",
            "if a > b:",
            "    print('a is greater than b')",
            "elif a < b:",
            "    print('a is less than b')",
            "else:",
            "    print('a is equal to b')",
            "    class MyClass(object):",
            "        def __init__(self, x):",
            "            self.x = x",
            "        def get_x(self):",
            "            return self.x"
        ]
    },
    {
        "class": "Import",
        "modules": ["math", "os"]
    },
    {
        "class": "Comparison",
        "left": "a",
        "operator": ">",
        "right": "b"
    },
    {
        "class": "WhileLoop",
        "condition": "a < 10",
        "body": [
            "print(a)",
            "a += 1"
        ]
    },
    {
        "class": "Conditional",
        "condition": "a < 5",
        "body": [
            "print('a is less than 5')",
            "print('a is less than 5')"
        ],
        "elif_condition": "a == 5",
        "elif_body": [
            "print('a is equal to 5')",
            "print('a is equal to 5')"
        ],
        "else_body": [
            "print('a is greater than 5')",
            "print('a is equal to 5')"
        ]
    }
]

# Создание экземпляра класса CodeGenerator и генерация кода
generator = CodeGenerator()
generated_code = generator.generate_code(input_data)
# Вывод сгенерированного кода на экран
print(generated_code)
