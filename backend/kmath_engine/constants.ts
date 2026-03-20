export const CATEGORIES = [
  { id: 'KR_Middle', name: '중학교' },
  { id: 'KR_High', name: '고등학교' },
  { id: 'AMC', name: 'AMC' },
];

export const GRADES_MAP: Record<string, { id: string, name: string }[]> = {
  'KR_Middle': [
    { id: 'Middle_1-1', name: '1학년 1학기' },
    { id: 'Middle_1-2', name: '1학년 2학기' },
    { id: 'Middle_2-1', name: '2학년 1학기' },
    { id: 'Middle_2-2', name: '2학년 2학기' },
    { id: 'Middle_3-1', name: '3학년 1학기' },
    { id: 'Middle_3-2', name: '3학년 2학기' },
  ],
  'KR_High': [{ id: 'High_Common', name: '공통수학' }],
  'AMC': [{ id: 'AMC_8', name: 'AMC 8' }]
};

export const ALL_STANDARDS = [
  { id: 'STD-11-01', name: '소인수분해의 이해', grade: 'Middle_1-1' },
  { id: 'STD-11-02', name: '최대공약수와 최소공배수', grade: 'Middle_1-1' },
  { id: 'STD-11-03', name: '정수와 유리수의 뜻과 대소 관계', grade: 'Middle_1-1' },
  { id: 'STD-11-04', name: '유리수의 사칙계산', grade: 'Middle_1-1' },
  { id: 'STD-11-05', name: '문자의 사용과 식의 값', grade: 'Middle_1-1' },
  { id: 'STD-11-06', name: '일차식의 계산', grade: 'Middle_1-1' },
  { id: 'STD-11-07', name: '일차방정식의 풀이', grade: 'Middle_1-1' },
  { id: 'STD-11-08', name: '일차방정식의 활용', grade: 'Middle_1-1' },
  { id: 'STD-11-09', name: '좌표와 그래프', grade: 'Middle_1-1' },
  { id: 'STD-11-10', name: '정비례와 반비례', grade: 'Middle_1-1' },
  // 1-2학기
  { id: 'STD-12-01', name: '점, 선, 면, 각', grade: 'Middle_1-2' },
  { id: 'STD-12-02', name: '위치 관계', grade: 'Middle_1-2' },
  { id: 'STD-12-03', name: '작도와 합동', grade: 'Middle_1-2' },
  { id: 'STD-12-04', name: '다각형', grade: 'Middle_1-2' },
  { id: 'STD-12-05', name: '원과 부채꼴', grade: 'Middle_1-2' },
  { id: 'STD-12-06', name: '다면체와 회전체', grade: 'Middle_1-2' },
  { id: 'STD-12-07', name: '입체도형의 겉넓이와 부피', grade: 'Middle_1-2' },
  { id: 'STD-12-08', name: '자료의 정리와 해석', grade: 'Middle_1-2' },
  // 2-1학기
  { id: 'STD-21-01', name: '유리수와 순환소수', grade: 'Middle_2-1' },
  { id: 'STD-21-02', name: '단항식의 계산', grade: 'Middle_2-1' },
  { id: 'STD-21-03', name: '다항식의 계산', grade: 'Middle_2-1' },
  { id: 'STD-21-04', name: '일차부등식', grade: 'Middle_2-1' },
  { id: 'STD-21-05', name: '일차부등식의 활용', grade: 'Middle_2-1' },
  { id: 'STD-21-06', name: '연립일차방정식', grade: 'Middle_2-1' },
  { id: 'STD-21-06', name: '연립일차방정식', grade: 'Middle_2-1' },
  // 고등 공통수학
  { id: 'STD-HIGH-01', name: '복소수와 이차방정식', grade: 'High_Common' },
];