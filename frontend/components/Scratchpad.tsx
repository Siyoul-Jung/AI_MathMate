'use client';

import React, { useRef, useState, useEffect } from 'react';

interface ScratchpadProps {
  isActive: boolean;
  onClose: () => void;
}

export default function Scratchpad({ isActive, onClose }: ScratchpadProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [context, setContext] = useState<CanvasRenderingContext2D | null>(null);
  const [color, setColor] = useState('#ef4444'); // Default: Red
  const [lineWidth, setLineWidth] = useState(3); // Default: Normal

  // Canvas initialization and resizing handling
  useEffect(() => {
    const canvas = canvasRef.current;
    if (canvas && isActive) {
      const ctx = canvas.getContext('2d');
      if (ctx) {
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
        ctx.strokeStyle = color;
        ctx.lineWidth = lineWidth;
        setContext(ctx);
      }

      const handleResize = () => {
        const parent = canvas.parentElement;
        if (parent) {
          // Match canvas size to parent element (problem area)
          // Note: Since content is reset when canvas size changes, actual implementation might need logic to save/restore image data
          const tempImage = ctx?.getImageData(0, 0, canvas.width, canvas.height);
          canvas.width = parent.clientWidth;
          canvas.height = parent.clientHeight;
          
          if (ctx) {
             // Reset context properties after resize
            ctx.lineCap = 'round';
            ctx.lineJoin = 'round';
            ctx.strokeStyle = color;
            ctx.lineWidth = lineWidth;
            if (tempImage) ctx.putImageData(tempImage, 0, 0);
          }
        }
      };

      handleResize();
      window.addEventListener('resize', handleResize);
      return () => window.removeEventListener('resize', handleResize);
    }
  }, [isActive]); // Run only on initialization and resize (excluding color, lineWidth dependencies)

  // Update context when color or line width changes
  useEffect(() => {
    if (context) {
      context.strokeStyle = color;
      context.lineWidth = lineWidth;
    }
  }, [context, color, lineWidth]);

  const startDrawing = (e: React.MouseEvent | React.TouchEvent) => {
    if (!context) return;
    setIsDrawing(true);
    const { x, y } = getPos(e);
    context.beginPath();
    context.moveTo(x, y);
  };

  const draw = (e: React.MouseEvent | React.TouchEvent) => {
    if (!isDrawing || !context) return;
    const { x, y } = getPos(e);
    context.lineTo(x, y);
    context.stroke();
  };

  const stopDrawing = () => {
    setIsDrawing(false);
    context?.closePath();
  };

  const getPos = (e: React.MouseEvent | React.TouchEvent) => {
    const canvas = canvasRef.current;
    if (!canvas) return { x: 0, y: 0 };
    const rect = canvas.getBoundingClientRect();
    const clientX = 'touches' in e ? e.touches[0].clientX : (e as React.MouseEvent).clientX;
    const clientY = 'touches' in e ? e.touches[0].clientY : (e as React.MouseEvent).clientY;
    return {
      x: clientX - rect.left,
      y: clientY - rect.top
    };
  };

  const clearCanvas = () => {
    if (context && canvasRef.current) {
      context.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
    }
  };

  if (!isActive) return null;

  return (
    <div className="absolute inset-0 z-20 pointer-events-none overflow-hidden rounded-xl border-2 border-blue-400 bg-transparent shadow-md">
      {/* Toolbar */}
      <div className="absolute top-4 right-4 flex flex-col gap-2 pointer-events-auto items-end">
        {/* Color and Thickness Selection */}
        <div className="bg-white/90 backdrop-blur p-2 rounded-lg shadow-sm border border-slate-200 flex gap-3 items-center">
          <div className="flex gap-1">
            {[
              { c: '#1e293b', label: 'Black' },
              { c: '#ef4444', label: 'Red' },
              { c: '#3b82f6', label: 'Blue' },
              { c: '#22c55e', label: 'Green' }
            ].map((item) => (
              <button
                key={item.c}
                onClick={() => setColor(item.c)}
                className={`w-6 h-6 rounded-full border-2 transition-transform hover:scale-110 ${color === item.c ? 'border-slate-400 scale-110' : 'border-transparent'}`}
                style={{ backgroundColor: item.c }}
                title={item.label}
              />
            ))}
          </div>
          <div className="w-px h-4 bg-slate-300 mx-1"></div>
          <div className="flex gap-1 items-center">
            {[2, 4, 8].map((w) => (
              <button
                key={w}
                onClick={() => setLineWidth(w)}
                className={`w-6 h-6 flex items-center justify-center rounded hover:bg-slate-100 ${lineWidth === w ? 'bg-slate-100 ring-1 ring-slate-300' : ''}`}
              >
                <div className="bg-slate-800 rounded-full" style={{ width: w, height: w }} />
              </button>
            ))}
          </div>
        </div>

        <div className="flex gap-2">
        <button 
          onClick={clearCanvas}
          className="bg-white/90 backdrop-blur text-slate-700 px-3 py-1.5 rounded-lg shadow-sm border border-slate-200 text-xs font-bold hover:bg-slate-50 transition-colors"
        >
          🗑️ Clear
        </button>
        <button 
          onClick={onClose}
          className="bg-slate-800 text-white px-3 py-1.5 rounded-lg shadow-sm text-xs font-bold hover:bg-slate-700 transition-colors"
        >
          ✕ Close
        </button>
        </div>
      </div>
      
      {/* Canvas */}
      <canvas
        ref={canvasRef}
        className="w-full h-full cursor-crosshair pointer-events-auto touch-none"
        onMouseDown={startDrawing}
        onMouseMove={draw}
        onMouseUp={stopDrawing}
        onMouseLeave={stopDrawing}
        onTouchStart={startDrawing}
        onTouchMove={draw}
        onTouchEnd={stopDrawing}
      />
    </div>
  );
}