"""Utility: remove docstrings and LICENSE files under Source_manim_reference

Caution: rewrites .py files in-place. Keeps a .bak copy before editing.
"""
import ast
import os
import shutil
import sys
import re

ROOT = os.path.join(os.path.dirname(__file__), '..', 'Source_manim_reference')
ROOT = os.path.abspath(ROOT)

class DocstringRemover(ast.NodeTransformer):
    def _strip_first_doc(self, node):
        if getattr(node, 'body', None):
            first = node.body[0]
            if isinstance(first, ast.Expr) and isinstance(first.value, (ast.Constant, ast.Str)) and isinstance(first.value.value, str):
                node.body.pop(0)

    def visit_Module(self, node):
        self.generic_visit(node)
        self._strip_first_doc(node)
        return node

    def visit_FunctionDef(self, node):
        self.generic_visit(node)
        self._strip_first_doc(node)
        return node

    def visit_AsyncFunctionDef(self, node):
        self.generic_visit(node)
        self._strip_first_doc(node)
        return node

    def visit_ClassDef(self, node):
        self.generic_visit(node)
        self._strip_first_doc(node)
        return node

def remove_docstrings_explicit(tree):
    # Remove docstrings using ast.get_docstring check for Module/Class/Function
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            try:
                ds = ast.get_docstring(node, clean=False)
            except Exception:
                ds = None
            if ds is not None and getattr(node, 'body', None):
                first = node.body[0]
                if isinstance(first, ast.Expr) and isinstance(first.value, (ast.Constant, ast.Str)) and isinstance(getattr(first.value, 'value', None), str):
                    node.body.pop(0)


def process_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            src = f.read()
    except Exception as e:
        print(f"SKIP read {path}: {e}")
        return
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        print(f"SKIP parse {path}: {e}")
        return
    remover = DocstringRemover()
    new_tree = remover.visit(tree)
    # additional pass: explicit removal via ast.get_docstring checks
    remove_docstrings_explicit(new_tree)
    ast.fix_missing_locations(new_tree)
    try:
        new_src = ast.unparse(new_tree)
    except Exception as e:
        print(f"UNPARSE failed for {path}: {e}")
        return
    # Quick check: if identical, skip
    if new_src.strip() == src.strip():
        return
    # Backup
    bak = path + '.bak'
    try:
        shutil.copy2(path, bak)
    except Exception as e:
        print(f"Could not make backup for {path}: {e}")
        return
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_src)
        print(f"UPDATED {path}")
    except Exception as e:
        print(f"WRITE failed {path}: {e}")
        # try to restore
        try:
            shutil.move(bak, path)
        except Exception:
            pass


def main():
    if not os.path.isdir(ROOT):
        print("Source_manim_reference not found at", ROOT)
        sys.exit(1)
    removed_license = 0
    updated = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        for fn in filenames:
            path = os.path.join(dirpath, fn)
            low = fn.lower()
            if low.startswith('license') or low == 'license.txt' or low == 'license':
                try:
                    os.remove(path)
                    removed_license += 1
                    print(f"REMOVED LICENSE {path}")
                except Exception as e:
                    print(f"FAILED remove license {path}: {e}")
                continue
            if fn.endswith('.py'):
                process_file(path)
                updated += 1
    # Second pass: remove any remaining triple-quoted blocks by regex (fallback)
    triple_re = re.compile(r"('''.*?'''|\"\"\".*?\"\"\")", re.S)
    regex_removed = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        for fn in filenames:
            if not fn.endswith('.py'):
                continue
            path = os.path.join(dirpath, fn)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    src = f.read()
            except Exception:
                continue
            new_src = triple_re.sub('', src)
            if new_src != src:
                bak = path + '.bak_regex'
                try:
                    shutil.copy2(path, bak)
                except Exception:
                    pass
                try:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_src)
                    regex_removed += 1
                    print(f"REGEX-REMOVED triples in {path}")
                except Exception as e:
                    print(f"Failed regex write {path}: {e}")

    print(f"Done. processed {updated} py files, removed {removed_license} license files, regex-cleaned {regex_removed} files")

if __name__ == '__main__':
    main()
