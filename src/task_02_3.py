def check_brackets(expression: str) -> str:
    stack = []
    matching_bracket = {")": "(", "}": "{", "]": "["}

    for char in expression:
        if char in "({[":
            stack.append(char)
        elif char in ")}]":
            if not stack or stack.pop() != matching_bracket[char]:
                return "Несиметрично"

    return "Симетрично" if not stack else "Несиметрично"


# Тестування функції
test_expressions = [
    "( ){[ 1 ]( 1 + 3 )( ){ }}",
    "( 23 ( 2 - 3);",
    "( 11 }",
    "[{()}]",
    "((()))",
    "[[[]]]",
    "({[)]}",
]

for expr in test_expressions:
    print(f"'{expr}': {check_brackets(expr)}")
