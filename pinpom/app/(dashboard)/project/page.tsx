import { Navbar } from "@/components/common/navbar";
import { Sidebar } from "@/components/common/sidebar";
import { routes } from "@/constants/route";

export default function ProjectOverview() {
  return (
    <>
      <header>
        <Navbar />
      </header>
      <div className='flex h-full'>
        <aside>
          <Sidebar routes={routes} />
        </aside>
        <main>
          main
        </main>
      </div>
    </>
  );
}