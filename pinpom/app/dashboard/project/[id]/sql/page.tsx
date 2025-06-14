import { MonacoEditor } from "@/components/sql-editor/monaco-editor";
import { ViewData } from "@/components/sql-editor/view-data";
import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from "@/components/ui/resizable";

export default function SQLEditorPage() {
  return (
    <ResizablePanelGroup direction="vertical" className="flex-1 w-full h-full">
      <ResizablePanel defaultSize={60}>
        <div className="h-full w-full">
          <MonacoEditor />
        </div>
      </ResizablePanel>
      <ResizableHandle withHandle />
      <ResizablePanel defaultSize={40}>
        <div className="h-full w-full">
          <ViewData />
        </div>
      </ResizablePanel>
    </ResizablePanelGroup>
  );
}