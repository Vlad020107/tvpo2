import dis
import importlib.util
import sys
from pathlib import Path
import pytest

path = Path(__file__).resolve().parent / 'text_analyzer.py'
spec = importlib.util.spec_from_file_location('text_analyzer', path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
sys.modules['text_analyzer'] = module

def executable(code):
    lines = {line for _, line in dis.findlinestarts(code) if line is not None}
    for constant in code.co_consts:
        if isinstance(constant, type(code)):
            lines |= executable(constant)
    return lines

compiled = compile(path.read_text(encoding='utf-8'), str(path), 'exec')
possible = executable(compiled)
visited = set()
def tracer(frame, event, arg):
    if event == 'line' and frame.f_code.co_filename == str(path):
        visited.add(frame.f_lineno)
    return tracer

sys.settrace(tracer)
status = pytest.main(['-q', 'test_initial.py', 'test_improved.py'])
sys.settrace(None)
print(f'Строки модуля: {len(visited & possible)}/{len(possible)}; покрытие {100 * len(visited & possible) / len(possible):.1f}%; непокрытые: {sorted(possible - visited)}')
sys.exit(status)
