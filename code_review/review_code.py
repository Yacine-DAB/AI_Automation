import ast
import pycodestyle


class CodeReviewer:
    def __init__(self):
        self.feedback = []

    def analyze_python_code(self, code):
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            self.feedback.append(f"Syntax Error on line {e.lineno}: {e.msg}")
            return

        self._check_docstrings(tree)
        self._check_undefined_vars(tree)
        self._check_code_style(code)
        self._check_comments(code)

    def _check_docstrings(self, tree):
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if not ast.get_docstring(node):
                    self.feedback.append(f"{node.__class__.__name__} '{node.name}' is missing a docstring.")

    def _check_undefined_vars(self, tree):
        defined_vars = set()
        used_vars = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                if isinstance(node.ctx, ast.Store):
                    defined_vars.add(node.id)
                elif isinstance(node.ctx, ast.Load):
                    used_vars.add(node.id)
        
        undefined_vars = used_vars - defined_vars
        for var in undefined_vars:
            self.feedback.append(f"Variable '{var}' is used but not defined.")

    def _check_code_style(self, code):
          style_guide = pycodestyle.StyleGuide(quiet=True)
          style_errors = style_guide.check_files([code])
          for error in style_errors.get_statistics(''):
               self.feedback.append(f"Style Issue: {error}")

    def _check_comments(self, code):
        lines = code.split('\n')
        for i, line in enumerate(lines):
            if line.strip().startswith('#'):
                if len(line.strip()) == 1 or line.strip()[1] != ' ':
                    self.feedback.append(f"Improve comment style in line {i + 1}: '{line.strip()}'")

    def get_feedback(self):
        return self.feedback


if __name__ == "__main__":
    # Example Python code to analyze
    python_code = """
    def add(a, b):
        result = a + b
        print(result)
    """

    code_reviewer = CodeReviewer()
    code_reviewer.analyze_python_code(python_code)

    feedback = code_reviewer.get_feedback()

    if feedback:
        print("Code Review Feedback:")
        for msg in feedback:
            print(f"- {msg}")
    else:
        print("No coding errors found. Code looks good!")
