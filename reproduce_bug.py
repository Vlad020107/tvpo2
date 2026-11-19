import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

root = Path(__file__).resolve().parent
with TemporaryDirectory() as directory:
    work = Path(directory)
    fixed = (root / 'text_analyzer.py').read_text(encoding='utf-8')
    buggy = fixed.replace('return len(_words(text))', 'return len(text.split(" "))', 1)
    (work / 'text_analyzer.py').write_text(buggy, encoding='utf-8')
    (work / 'test_initial.py').write_bytes((root / 'test_initial.py').read_bytes())
    result = subprocess.run([sys.executable, '-m', 'pytest', '-q', 'test_initial.py'], cwd=work)
    sys.exit(result.returncode)
