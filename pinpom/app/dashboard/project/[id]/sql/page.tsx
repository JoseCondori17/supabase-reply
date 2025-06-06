import { SidebarContent } from "@/components/common/sidebar-content";

export default function SQLEditorPage() {
  return (
    <div className='flex w-full'>
      <SidebarContent title='SQL Editor' items={[]} />
      <div className='flex-1 flex'>
        editor
      </div>
    </div>
  );
}