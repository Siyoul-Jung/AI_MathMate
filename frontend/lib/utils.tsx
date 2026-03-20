import React from 'react';
import { InlineMath, BlockMath } from 'react-katex';

// Text parsing helper (Bold, Newline)
export const parseText = (text: string) => {
  return text.split(/(\*\*.*?\*\*|\n)/g).map((part, i) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={i}>{part.slice(2, -2)}</strong>;
    }
    if (part === '\n') return <br key={i} />;
    return <span key={i}>{part}</span>;
  });
};

// Improved rendering function (Supports HTML, Block Math, Inline Math)
export const renderContent = (text: string) => {
  if (!text) return null;
  
  // 1. Block Math ($$ ... $$ 또는 \[ ... \]) 분리
  const blocks = text.split(/(\$\$[\s\S]*?\$\$|\\\[[\s\S]*?\\\])/g);
  
  return blocks.map((block, i) => {
    // $$ ... $$ 또는 \[ ... \] 처리
    if ((block.startsWith('$$') && block.endsWith('$$')) || (block.startsWith('\\[') && block.endsWith('\\]'))) {
      const math = block.startsWith('$$') ? block.slice(2, -2) : block.slice(2, -2);
      return <div key={i} className="my-2"><BlockMath math={math} /></div>;
    }
    
    const htmlParts = block.split(/(<div[\s\S]*?<\/div>)/g);
    return htmlParts.map((htmlPart, j) => {
      if (htmlPart.startsWith('<div') && htmlPart.endsWith('</div>')) return <div key={`${i}-${j}`} dangerouslySetInnerHTML={{ __html: htmlPart }} />;
      
      // 2. Separate Inline Math ($ ... $ or \( ... \))
      const inlineParts = htmlPart.split(/(\$[\s\S]*?\$|\\\([\s\S]*?\\\))/g);
      return inlineParts.map((part, k) => {
        if ((part.startsWith('$') && part.endsWith('$')) || (part.startsWith('\\(') && part.endsWith('\\)'))) {
          const math = part.startsWith('$') ? part.slice(1, -1) : part.slice(2, -2);
          return <InlineMath key={`${i}-${j}-${k}`} math={math} />;
        }
        return <span key={`${i}-${j}-${k}`}>{parseText(part)}</span>;
      });
    });
  });
};
