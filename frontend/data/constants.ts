'use client';

export const CATEGORIES = [
  { id: 'AMC_10', name: 'AMC 10' },
  { id: 'AMC_12', name: 'AMC 12' },
  { id: 'AIME', name: 'AIME' },
];

export const GRADES_MAP: Record<string, { id: string, name: string }[]> = {
  'AMC_10': [
    { id: 'AMC_10_E', name: 'Elementary/Middle' },
    { id: 'AMC_10_H', name: 'High School' }
  ],
  'AMC_12': [
    { id: 'AMC_12_H', name: 'High School' }
  ],
  'AIME': [
    { id: 'AIME_1', name: 'AIME 1' }
  ]
};

export const ALL_STANDARDS = [
  { id: 'STD-AIME-2025-1', name: 'AIME 2025 I Drills', grade: 'AIME_1' },
  // Grade 7 Semester 1
  { id: 'STD-11-01', name: 'Prime Factorization', grade: 'Middle_1-1' },
  { id: 'STD-11-02', name: 'GCD and LCM', grade: 'Middle_1-1' },
  { id: 'STD-11-03', name: 'Integers & Rational Numbers', grade: 'Middle_1-1' },
  { id: 'STD-11-04', name: 'Rational Number Arithmetic', grade: 'Middle_1-1' },
  { id: 'STD-11-05', name: 'Algebraic Expressions', grade: 'Middle_1-1' },
  { id: 'STD-11-06', name: 'Linear Expression Ops', grade: 'Middle_1-1' },
  { id: 'STD-11-07', name: 'Solving Linear Equations', grade: 'Middle_1-1' },
  { id: 'STD-11-08', name: 'Linear Equation Apps', grade: 'Middle_1-1' },
  { id: 'STD-11-09', name: 'Coordinates & Graphs', grade: 'Middle_1-1' },
  { id: 'STD-11-10', name: 'Proportion & Inverse', grade: 'Middle_1-1' },
  // Grade 7 Semester 2
  { id: 'STD-12-01', name: 'Points, Lines, Planes, Angles', grade: 'Middle_1-2' },
  { id: 'STD-12-02', name: 'Spatial Relationships', grade: 'Middle_1-2' },
  { id: 'STD-12-03', name: 'Construction & Congruence', grade: 'Middle_1-2' },
  { id: 'STD-12-04', name: 'Polygons', grade: 'Middle_1-2' },
  { id: 'STD-12-05', name: 'Circles & Sectors', grade: 'Middle_1-2' },
  { id: 'STD-12-06', name: 'Polyhedrons & Rotation', grade: 'Middle_1-2' },
  { id: 'STD-12-07', name: 'Surface Area & Volume', grade: 'Middle_1-2' },
  { id: 'STD-12-08', name: 'Data & Interpretation', grade: 'Middle_1-2' },
  // Grade 8 Semester 1
  { id: 'STD-21-01', name: 'Rational & Repeating Decimals', grade: 'Middle_2-1' },
  { id: 'STD-21-02', name: 'Monomial Operations', grade: 'Middle_2-1' },
  { id: 'STD-21-03', name: 'Polynomial Operations', grade: 'Middle_2-1' },
  { id: 'STD-21-04', name: 'Linear Inequalities', grade: 'Middle_2-1' },
  { id: 'STD-21-05', name: 'Linear Inequality Apps', grade: 'Middle_2-1' },
  { id: 'STD-21-07', name: 'Solving Systems of Equations', grade: 'Middle_2-1' },
  { id: 'STD-21-08', name: 'Systems of Equations Apps', grade: 'Middle_2-1' },
  // High School Common Math 1
  { id: 'STD-HIGH-01', name: 'I. Polynomials', grade: 'High_Common_1' },
  { id: 'STD-HIGH-02', name: 'II. Equ. & Inequ. (Complex/Quad)', grade: 'High_Common_1' },
  { id: 'STD-HIGH-06', name: 'III. Combinatorics', grade: 'High_Common_1' },
  { id: 'STD-HIGH-07', name: 'IV. Matrices', grade: 'High_Common_1' },
  // High School Common Math 2
  { id: 'STD-HIGH-08', name: 'V. Analytic Geometry (Plane)', grade: 'High_Common_2' },
  { id: 'STD-HIGH-13', name: 'VI. Logic & Sets', grade: 'High_Common_2' },
  { id: 'STD-HIGH-14', name: 'VII. Functions & Inverse', grade: 'High_Common_2' },
  { id: 'STD-HIGH-15', name: 'VIII. Rational & Irrational Func', grade: 'High_Common_2' },
];