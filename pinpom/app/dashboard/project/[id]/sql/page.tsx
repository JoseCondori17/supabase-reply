import { SidebarContent } from "@/components/common/sidebar-content";
import { MonacoEditor } from "@/components/sql-editor/monaco-editor";
import { ViewData } from "@/components/sql-editor/view-data";
import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from "@/components/ui/resizable"

export default function SQLEditorPage() {
  return (
    <div className='flex w-full'>
      <SidebarContent title='SQL Editor' items={[]} />
      <ResizablePanelGroup direction="vertical">
        <ResizablePanel>
          <MonacoEditor/>
        </ResizablePanel>
        <ResizableHandle withHandle/>
        <ResizablePanel>
          <ViewData/>
        </ResizablePanel>
      </ResizablePanelGroup>
    </div>
  );
}