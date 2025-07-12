'use client';

import Editor from '@monaco-editor/react';

interface MonacoEditorProps {
  value: string;
  onChange: (value: string) => void;
}

export function MonacoEditor({ value, onChange }: MonacoEditorProps) {
  return (
    <div className="h-full w-full overflow-hidden">
      <Editor
        language='pgsql'
        value={value}
        onChange={(val) => onChange(val || "")}
        options={{
          minimap: { enabled: false },
          scrollBeyondLastLine: false,
          automaticLayout: true,
          wordWrap: 'on',
          lineNumbers: 'on',
          folding: true,
          fontSize: 14,
        }}
        className="h-full w-full"
      />
    </div>
  );
}