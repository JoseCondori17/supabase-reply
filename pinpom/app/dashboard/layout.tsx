import { Navbar } from "@/components/common/navbar";
import { Sidebar } from "@/components/common/sidebar";
import { Toaster } from "@/components/ui/sonner";
import { routes } from "@/constants/route";

interface DashboardLayoutProps {
  children: React.ReactNode
}

export default function DashboardLayout(
  { children }: DashboardLayoutProps
) {
  return (
    <div className="flex flex-col h-screen w-screen">
      <header>
        <Navbar />
      </header>
      <div className='flex h-full'>
        <aside>
          <Sidebar routes={routes('orxhacgauokkkcbrgcxw')} />
        </aside>
        <main className='flex-1 flex h-full min-w-0 overflow-hidden'>
          {children}
        </main>
      </div>
      <Toaster />
    </div>
  );
}