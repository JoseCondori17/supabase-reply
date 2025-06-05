'use client'
import { buttonVariants } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { type RouteGroup } from "@/constants/route";
import { cn } from "@/lib/utils";
import type { LucideIcon } from 'lucide-react';
import * as lucideIcons from 'lucide-react';
import Link from "next/link";
import { usePathname } from "next/navigation";

interface SidebarProps {
  routes: RouteGroup[]
}

export function Sidebar({ routes }: SidebarProps) {
  const pathname = usePathname();

  return (
    <nav className='flex flex-col gap-1 border-r h-full'>
      <ul>
        {routes.map((group) => (
          <div key={group.label} className='flex flex-col min-w-0 gap-0.5'>
            <div className='flex flex-col w-full p-2 gap-0.5'>
              {group.routes.map((route) => {
                const Icon = lucideIcons[route.icon as keyof typeof lucideIcons] as LucideIcon;
                return (
                  <li key={route.path} className='flex items-center justify-center w-full'>
                    <Link
                      href={route.path}
                      className={cn(
                        buttonVariants({ variant: 'ghost', size: 'icon', className: 'flex items-center h-8 w-8 rounded-sm' }),
                        pathname === route.path && 'dark:bg-accent/50 bg-accent'
                      )}
                    >
                      <Icon className='size-5 stroke-1' />
                    </Link>
                  </li>
                );
              })}
            </div>
            <Separator />
          </div>
        ))}
      </ul>
    </nav>
  );
}