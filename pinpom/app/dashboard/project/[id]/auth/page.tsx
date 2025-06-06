import { SidebarContent } from "@/components/common/sidebar-content";
import { route_authentication } from "@/constants/route";

export default function AuthenticationPage() {
  return (
    <div className='w-full'>
      <SidebarContent title='Authentication' items={route_authentication('orxhacgauokkkcbrgcxw')} />
    </div>
  );
}