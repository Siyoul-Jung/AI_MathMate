import os
import sys
try:
    import yaml
except ImportError as e:
    yaml = None
    print(f"Warning: PyYAML import failed: {e}")
    print(f"Current Python: {sys.executable}")
try:
    import jinja2
except ImportError as e:
    jinja2 = None
    print(f"Warning: Jinja2 import failed: {e}")
import random
import traceback
from sympy import *

# BaseTMaster가 kmath_engine.base에 있다고 가정하고 import 시도
try:
    from kmath_engine.base import BaseTMaster
except ImportError:
    # fallback for standalone testing
    class BaseTMaster:
        def __init__(self, spec_id, title):
            self.spec_id = spec_id
            self.name = titlei
        def _format_response(self, data, q_type, difficulty):
            return data

class TemplateBasedMaster(BaseTMaster):
    """
    Markdown 템플릿 파일을 읽어 문제를 생성하는 마스터 클래스
    """
    def __init__(self, file_path, context_data=None):
        self.file_path = file_path
        self.context_data = context_data or {}
        self.meta = {}
        self.template_content = ""
        self.logic_code = ""
        self.parse_error = None
        self._parse_file()
        
        # BaseTMaster 초기화
        super().__init__(self.meta.get('id', 'UNKNOWN'), self.meta.get('title', 'Untitled'))

    def _parse_file(self):
        """Markdown 파일의 Frontmatter와 본문을 분리하여 파싱"""
        if yaml is None:
            print(f"Error: Cannot parse {self.file_path} because PyYAML is missing.")
            return

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    self.meta = yaml.safe_load(parts[1])
                    self.template_content = parts[2].strip()
                    self.logic_code = self.meta.get('logic_setup', '')
            else:
                self.template_content = content
        except Exception as e:
            print(f"Error parsing template {self.file_path}: {e}")
            self.parse_error = str(e)

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 1. 실행 컨텍스트 설정
        diff_map = {"Easy": 1, "Normal": 3, "Hard": 5}
        user_level = diff_map.get(difficulty, 3)
        
        # print(f"[DEBUG] Difficulty: {difficulty} -> User Level: {user_level}")

        exec_globals = {
            "user_level": user_level,
            "question_type": q_type,
            "random": random,
            "Matrix": Matrix,
            "latex": latex,
            "symbols": symbols,
            "solve": solve,
            "pi": pi,
            "sin": sin,
            "cos": cos,
            "sqrt": sqrt,
            "injected_context": {}
        }

        # 2. 외부 컨텍스트 주입 (context_master.json)
        req_ctx_key = self.meta.get('required_context')
        if req_ctx_key and req_ctx_key in self.context_data:
            exec_globals['injected_context'] = self.context_data[req_ctx_key]

        if self.parse_error:
            return {
                "error": f"Template Parsing Error in {os.path.basename(self.file_path)}",
                "details": self.parse_error,
                "question": f"(오류: 템플릿 파싱 실패. 파일: {os.path.basename(self.file_path)} - {self.parse_error})"
            }

        # 3. Python 로직 실행
        try:
            # Python 3의 exec()에서 globals와 locals를 분리하면,
            # 리스트 컴프리헨션 내부에서 로컬 변수(함수 포함)를 참조할 수 없는 스코프 문제가 발생합니다.
            # 따라서 하나의 딕셔너리로 통합하여 실행합니다.
            exec_context = exec_globals.copy()
            exec(self.logic_code, exec_context)
            exec_locals = exec_context
        except Exception as e:
            print(f"[Template Error] File: {self.file_path}\nError: {e}")
            return {
                "error": f"Logic Execution Error in {self.spec_id}",
                "details": str(e),
                "trace": traceback.format_exc()
            }

        # 4. 렌더링 변수 준비
        # render_vars가 명시되지 않았을 경우, 전체 로컬 변수를 사용하여 렌더링 (유연성 확보)
        render_vars = exec_locals.get('render_vars', exec_locals)
        
        # 객관식 보기 생성 로직
        if q_type in ['multiple_choice', 'multi']:
            ans_val = exec_locals.get('ans_val', exec_locals.get('answer'))
            distractors = exec_locals.get('distractors', [])
            options = [str(ans_val)] + [str(d) for d in distractors]
            options = list(set(options)) # 중복 제거
            random.shuffle(options)
            
            for i, opt in enumerate(options[:5]):
                render_vars[f'opt{i+1}'] = opt
            exec_locals['options_list'] = options

        # 5. 템플릿 렌더링 (질문 텍스트 생성)
        # 템플릿의 정답 노출 부분을 숨기기 위해 question_type을 임의로 변경하여 렌더링
        render_vars['question_type'] = 'generate_text_only'
        
        if not self.template_content:
             question_text = f"(오류: 템플릿 본문이 비어있습니다. 파일: {os.path.basename(self.file_path)})"
        elif jinja2:
            template = jinja2.Template(self.template_content)
            try:
                question_text = template.render(**render_vars).strip()
                if not question_text:
                    question_text = f"(오류: 템플릿 렌더링 결과가 비어있습니다. 파일: {os.path.basename(self.file_path)})"
            except Exception as e:
                print(f"[Template Render Error] File: {self.file_path}\nError: {e}")
                question_text = f"Error rendering template: {str(e)}"
        else:
            question_text = "Error: Jinja2 library missing."

        # 6. 결과 반환
        data = {
            "question": question_text,
            "answer": str(exec_locals.get('ans_val', exec_locals.get('answer', ''))),
            "type": self.meta.get('type_tag', self.spec_id),
            "strategy": exec_locals.get('strategy', ''),
            "explanation": exec_locals.get('explanation', ''),
            "logic_steps": exec_locals.get('logic_steps', []),
        }
        
        if q_type in ['multiple_choice', 'multi']:
            data['options'] = exec_locals.get('options_list', [])

        # BaseTMaster의 포맷팅 사용
        if hasattr(super(), '_format_response'):
            return super()._format_response(data, q_type, difficulty)
        return data
