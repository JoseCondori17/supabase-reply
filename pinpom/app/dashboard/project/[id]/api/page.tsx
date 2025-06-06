import { SidebarContent } from "@/components/common/sidebar-content";
import { route_api_docs } from "@/constants/route";

export default function ApiDocsPage() {
  return (
    <div className='w-full'>
      <SidebarContent title='API Docs' items={route_api_docs('orxhacgauokkkcbrgcxw')} />
    </div>
  );
}