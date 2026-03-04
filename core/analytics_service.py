import sqlite3
import os
from typing import Dict, List

class AnalyticsService:
    """
    학생 학습 데이터(Student_Step_Log)를 관리하고 분석하는 서비스
    """
    def __init__(self, db_name="mathmate.db"):
        # DB 파일은 프로젝트 루트에 저장
        self.db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), db_name)
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Student_Step_Log 테이블 생성 (명세서 기반)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS student_step_log (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                standard_id TEXT NOT NULL,
                step_type TEXT NOT NULL, -- CONCEPT, CALC, STRATEGY
                success_status TEXT NOT NULL, -- SELF, HINTED, FAIL
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()

    def log_step(self, student_id: str, standard_id: str, step_type: str, success_status: str):
        """학습 이력 저장"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO student_step_log (student_id, standard_id, step_type, success_status)
            VALUES (?, ?, ?, ?)
        ''', (student_id, standard_id, step_type, success_status))
        
        conn.commit()
        conn.close()

    def analyze_proficiency(self, student_id: str) -> Dict[str, float]:
        """성취기준별 숙련도 분석 (0~100점)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 성취기준별, 상태별 카운트 조회
        cursor.execute('''
            SELECT standard_id, success_status, COUNT(*)
            FROM student_step_log
            WHERE student_id = ?
            GROUP BY standard_id, success_status
        ''', (student_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        # 점수 계산 로직: SELF=100%, HINTED=50%, FAIL=0%
        stats = {}
        for std_id, status, count in rows:
            if std_id not in stats:
                stats[std_id] = {"total_count": 0, "weighted_score": 0}
            
            stats[std_id]["total_count"] += count
            
            if status == "SELF":
                stats[std_id]["weighted_score"] += count * 1.0
            elif status == "HINTED":
                stats[std_id]["weighted_score"] += count * 0.5
            # FAIL adds 0
            
        proficiency = {}
        for std_id, data in stats.items():
            if data["total_count"] > 0:
                score = (data["weighted_score"] / data["total_count"]) * 100
                proficiency[std_id] = round(score, 1)
            else:
                proficiency[std_id] = 0.0
                
        return proficiency

    def get_weak_points(self, student_id: str, threshold=60.0, limit=3) -> List[str]:
        """숙련도가 특정 임계값 미만인 취약 성취기준 리스트 반환 (점수 낮은 순 정렬, 최대 limit개)"""
        prof = self.analyze_proficiency(student_id)
        # 점수가 낮은 순서대로 정렬
        sorted_weak = sorted([(std, score) for std, score in prof.items() if score < threshold], key=lambda x: x[1])
        # 상위 limit개만 반환
        return [std for std, score in sorted_weak[:limit]]