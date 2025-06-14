'use client'
import Editor from '@monaco-editor/react';

export function MonacoEditor() {
  return (
    <div className="h-full w-full overflow-hidden">
      <Editor
        defaultLanguage='pgsql'
        defaultValue="-- write your script"
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