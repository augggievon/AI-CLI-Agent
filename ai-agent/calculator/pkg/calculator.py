class Calculator:
    def __init__(self):
        # Precedence: Higher number means higher precedence
        self.precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

    def evaluate(self, tokens: list[str]) -> float | None:
        """
        Evaluates an infix expression given as a list of tokens (strings).
        Example tokens: ["3", "+", "2"]
        """
        values_stack = []
        ops_stack = []
        
        def apply_op():
            """Applies the operator at the top of ops_stack to the top two values."""
            op = ops_stack.pop()
            if len(values_stack) < 2:
                raise ValueError("Invalid expression: insufficient operands for operator " + op)
            right = values_stack.pop()
            left = values_stack.pop()
            
            if op == '+':
                values_stack.append(left + right)
            elif op == '-':
                values_stack.append(left - right)
            elif op == '*':
                values_stack.append(left * right)
            elif op == '/':
                if right == 0:
                    raise ZeroDivisionError("Division by zero")
                values_stack.append(left / right)
            else:
                raise ValueError(f"Unknown operator: {op}")

        for token in tokens:
            # Check if the token is a number (integer or float, potentially negative)
            try:
                value = float(token)
                # If conversion succeeds, treat it as a value
                values_stack.append(value)
                continue
            except ValueError:
                pass # Not a number, proceed to check if it's an operator or parenthesis

            # Handle operators
            if token in self.precedence:
                ops_stack.append(token)
                
                # While there is an operator at the top of the ops stack 
                # and its precedence is greater than or equal to the current operator's precedence
                while (ops_stack and 
                       ops_stack[-1] != '(' and 
                       self.precedence.get(ops_stack[-1], 0) >= self.precedence[token]):
                    apply_op()
                
                # Push the current operator
                ops_stack.append(token)
            
            # Handling parentheses (if required, though not explicitly tested in the original context)
            elif token == '(':
                ops_stack.append(token)
            elif token == ')':
                # Evaluate until the matching '(' is found
                while ops_stack and ops_stack[-1] != '(':
                    apply_op()
                
                if not ops_stack or ops_stack[-1] != '(':
                    raise ValueError("Mismatched parentheses")
                
                # Pop the '('
                ops_stack.pop()
                
                # After popping '(', if there's another operator, apply it
                if ops_stack and ops_stack[-1] in self.precedence:
                    # This handles cases like (A)(B) or A(B) if the structure allowed it, 
                    # but for standard infix, we just let the next token handle it.
                    pass

        # Process remaining operators
        while ops_stack:
            if ops_stack[-1] == '(':
                raise ValueError("Mismatched parentheses")
            apply_op()
            
        return values_stack[0] if values_stack else None