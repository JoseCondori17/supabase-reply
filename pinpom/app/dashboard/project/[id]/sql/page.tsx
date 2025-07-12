'use client'
import { MonacoEditor } from "@/components/sql-editor/monaco-editor";
import { ViewData } from "@/components/sql-editor/view-data";
import { Button } from "@/components/ui/button";
import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from "@/components/ui/resizable";
import { useState } from "react";

export default function SQLEditorPage() {
  const [sql, setSQL] = useState("-- write your script");
  const [result, setResult] = useState<any[]>([]);

  const handleRunQuery = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/query/sql", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ query: sql }),
      });

      const data = await res.json();
      if (data.success) {
        setResult(data.data);
      } else {
        alert("Query failed.");
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <ResizablePanelGroup direction="vertical" className="flex-1 w-full h-full">
      <ResizablePanel defaultSize={60}>
        <div className="h-full w-full flex flex-col">
          <div className="flex justify-end p-2">
            <Button onClick={handleRunQuery} size={'sm'}>Run SQL</Button>
          </div>
          <div className="flex-1">
            <MonacoEditor value={sql} onChange={setSQL} />
          </div>
        </div>
      </ResizablePanel>
      <ResizableHandle withHandle />
      <ResizablePanel defaultSize={40}>
        <div className="h-full w-full pt-4">
          <ViewData data={result} />
        </div>
      </ResizablePanel>
    </ResizablePanelGroup>
  );
}