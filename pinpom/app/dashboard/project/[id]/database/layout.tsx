import { SidebarContent } from "@/components/common/sidebar-content";
import { routes_database } from "@/constants/route";

interface DatabasePageProps {
  children: React.ReactNode
};

export default function DatabasePage({ children }: DatabasePageProps) {
  return (
    <div className='flex w-full'>
      <SidebarContent title='Database' items={routes_database('orxhacgauokkkcbrgcxw')} />
      <div className="h-full flex flex-col flex-1 overflow-y-auto overflow-x-hidden">{children}</div>
    </div>
  );
}