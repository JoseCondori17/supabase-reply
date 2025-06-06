import { SidebarContent } from "@/components/common/sidebar-content";
import { routes_database } from "@/constants/route";

export default function DatabasePage() {
  return (
    <div className='w-full'>
      <SidebarContent title='Database' items={routes_database('orxhacgauokkkcbrgcxw')} />
    </div>
  );
}