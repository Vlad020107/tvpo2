import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

root = Path(__file__).resolve().parent
original = (root / 'text_analyzer.py').read_text(encoding='utf-8')
mutations = {
    'M1_count_words_plus_one': ('return len(_words(text))', 'return len(_words(text)) + 1'),
    'M2_frequencies_unique': ('return dict(Counter(_words(text)))', 'return {word: 1 for word in _words(text)}'),
    'M3_characters_trim': ('return len(text)', 'return len(text.strip())'),
    'M4_casefold_to_lower': ('text.casefold()', 'text.lower()'),
    'M5_reverse_tiebreak': ('return min(frequencies, key=lambda word: (-frequencies[word], word))', 'return max(frequencies, key=lambda word: (frequencies[word], word))'),
    'M6_round_average': ('return sum(map(len, words)) / len(words)', 'return round(sum(map(len, words)) / len(words))'),
}
results = {}
for name, (old, new) in mutations.items():
    if original.count(old) != 1:
        raise RuntimeError(f'Невозможно однозначно применить {name}')
    with TemporaryDirectory() as directory:
        work = Path(directory)
        (work / 'text_analyzer.py').write_text(original.replace(old, new, 1), encoding='utf-8')
        for test in ('test_initial.py', 'test_improved.py'):
            (work / test).write_bytes((root / test).read_bytes())
        statuses = []
        for args in (['test_initial.py'], ['test_initial.py', 'test_improved.py']):
            process = subprocess.run([sys.executable, '-m', 'pytest', '-q', *args], cwd=work, capture_output=True, text=True)
            if process.returncode not in (0, 1):
                raise RuntimeError(f'{name}: ошибка инфраструктуры: {process.stdout} {process.stderr}')
            statuses.append('выжил' if process.returncode == 0 else 'убит')
        results[name] = statuses
        print(f'{name}: исходные — {statuses[0]}, дополненные — {statuses[1]}')
for column, label in ((0, 'До'), (1, 'После')):
    killed = sum(status[column] == 'убит' for status in results.values())
    print(f'{label}: {killed}/{len(results)} = {killed / len(results):.1%}')
