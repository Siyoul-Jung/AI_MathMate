import re

class LatexCleaner:
    @staticmethod
    def normalize(text):
        if not text: return text
        
        # 0. Recover characters eaten by control char interpretation
        text = text.replace('\b', '\\b')
        text = text.replace('\f', '\\f')
        text = text.replace('\t', '\\t')
        text = text.replace('\n', ' ')
        text = text.replace('\r', '')
        
        # Cleanup redundant literal \t artifacts
        text = text.replace('\\t\\text', '\\text')
        text = text.replace('\\t\\times', '\\times')
        text = text.replace('\\t \\times', '\\times')
        text = text.replace('\\t\\Delta', '\\Delta')
        text = text.replace('\\t\\angle', '\\angle')
        text = text.replace('\\t\\triangle', '\\triangle')
        text = text.replace('\\t\\frac', '\\frac')
        text = text.replace('\\t \\frac', '\\frac')
        text = text.replace('\\t ', ' ')
        
        # Aggressive backslash-t cleanup
        text = re.sub(r'\\t\s*\\', r'\\', text)

        # 1. Standardize delimiters
        text = re.sub(r'\\\((.*?)\\\)', r'$\1$', text)
        text = re.sub(r'\\\[(.*?)\\\]', r'$$\1$$', text, flags=re.DOTALL)
        
        # Cleanup repeated variables
        text = re.sub(r'\\+\s*\\+', r'\\', text)
        text = re.sub(r'\s{2,}', ' ', text)
        text = text.replace('a b a b', 'a\\sqrt{b}')
        
        # Cleanup specific Gemini hallucinations around triangle
        text = text.replace('\\ t \\ \\ t \\ triangle', '\\triangle')
        text = text.replace('\\ t \\ triangle', '\\triangle')
        text = text.replace('t \\ triangle', '\\triangle')
        text = text.replace('\\ \\t \\triangle', '\\triangle')
        text = text.replace('\\t \\triangle', '\\triangle')
        text = text.replace('\\t\\triangle', '\\triangle')
        
        # Cleanup missing line breaks in cases environments
        if '\\begin{cases}' in text:
            text = re.sub(r'(\d|\||\})\s*\\(\s*[\|0-9a-zA-Zx])', r'\1 \\\\ \2', text)
            text = re.sub(r'(\w)\s*\\\s*([\d\-])', r'\1 \\\\ \2', text)
            text = text.replace(r' \ |z', r' \\ |z')
            text = text.replace(r'\ |z', r' \\ |z')

        # 2. Fix Unicode math symbols
        unicode_map = {
            '⌊': r'\lfloor ', '⌋': r'\rfloor ',
            '⌈': r'\lceil ', '⌉': r'\rceil ',
            'θ': r'\theta ', 'α': r'\alpha ', 'β': r'\beta ', 'π': r'\pi ',
            '∆': r'\Delta ', '∠': r'\angle ', '⊥': r'\perp ',
            '±': r'\pm ', '×': r'\times ', '÷': r'\div ',
            '≤': r'\le ', '≥': r'\ge ', '≠': r'\ne ',
            '≈': r'\approx ', '∞': r'\infty ', '√': r'\sqrt ',
            '∈': r'\in ', '∉': r'\notin ', 'ℤ': r'\mathbb{Z}', 'ℝ': r'\mathbb{R}',
            '−': r'-', '·': r'\cdot '
        }
        for u_char, tex in unicode_map.items():
            text = text.replace(u_char, tex)
        
        # 3. Backslash Restoration
        word_cmds = [
            'le', 'ge', 'ne', 'pm', 'alpha', 'beta', 'theta', 'pi', 
            'Delta', 'triangle', 'angle', 'perp', 'approx', 'infty', 'cdot', 'mathbb{Z}', 'mathbb{R}'
        ]
        symbol_cmds = ['begin{cases}', 'end{cases}', 'text{', 'frac{', 'sqrt{', 'pmod{', 'times', 'circ']
        
        for cmd in word_cmds:
             pattern = r'(?<!\\)\b' + re.escape(cmd.strip()) + r'\b'
             text = re.sub(pattern, r'\\' + cmd.strip(), text)
             
        for cmd in symbol_cmds:
             pattern = r'(?<!\\)' + re.escape(cmd)
             text = re.sub(pattern, r'\\' + cmd, text)
        
        text = text.replace(' n in Z', r' n \in \mathbb{Z}')
        text = text.replace(' n \in Z', r' n \in \mathbb{Z}')

        # Fix spacing hallucinations
        text = re.sub(r'f\s*\(\s*x\s*\)', 'f(x)', text)
        text = re.sub(r'g\s*\(\s*x\s*\)', 'g(x)', text)
        text = re.sub(r'P\s*\(\s*x\s*\)', 'P(x)', text)
        
        # degree/symbol hallucinations
        text = text.replace('\\text{circ}', r'^\circ')
        text = text.replace('\\text{\\circ}', r'^\circ')
        text = text.replace('\\text{degree}', r'^\circ')
        
        # Systemic Deduplication
        text = text.replace('mod1000', r' \pmod{1000}')
        text = text.replace('mod 1000', r' \pmod{1000}')
        text = text.replace('modulo 1000', r' \pmod{1000}')
        text = text.replace('{reqs}', '').replace('reqs', '')
        
        text = re.sub(r'(\d+)\^\\circ\s+\1\^\\circ', r'\1^\\circ', text)
        text = re.sub(r'\b(\d+)\b\s+\1\b', r'\1', text)
        text = re.sub(r'\$([a-zA-Z])\$\s+\$\1\$', r'$\1$', text)
        text = re.sub(r'\b(\w{3,})\b\s+\1\b', r'\1', text)

        return text.strip()

    @staticmethod
    def validate(text):
        errors = []
        if not text: return errors
        if text.count('$') % 2 != 0:
            errors.append("Unbalanced math delimiters $")
        if text.count('{') - text.count('}') != 0:
            errors.append(f"Unbalanced braces {{}}: {text.count('{')} vs {text.count('}')}")
        env_starts = re.findall(r'\\begin\{(.*?)\}', text)
        env_ends = re.findall(r'\\end\{(.*?)\}', text)
        if len(env_starts) != len(env_ends):
            errors.append(f"Unbalanced environments: {len(env_starts)} vs {len(env_ends)}")
        return errors
