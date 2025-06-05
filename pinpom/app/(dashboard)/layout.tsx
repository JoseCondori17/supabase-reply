import { Toaster } from "@/components/ui/sonner";

interface DashboardLayoutProps {
  children: React.ReactNode
}

export default function DashboardLayout(
  { children }: DashboardLayoutProps
) {
  return (
    <div className="flex flex-col h-screen w-screen">
      {children}
      <Toaster />
    </div>
  );
}