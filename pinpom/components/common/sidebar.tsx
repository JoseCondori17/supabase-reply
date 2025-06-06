'use client'
import Link from "next/link";
import * as lucideIcons from 'lucide-react';
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import type { Route } from "@/constants/route";
import type { LucideIcon } from 'lucide-react';

import { buttonVariants } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip"

interface SidebarProps {
  routes: Route[]
};

function SibebarItem({ icon, label, path }: Route) {
  const pathname = usePathname();

  const Icon = lucideIcons[icon as keyof typeof lucideIcons] as LucideIcon;
  return (
    <li className='flex items-center justify-center w-full'>
      <Tooltip>
        <TooltipTrigger asChild>
          <Link
            href={path ?? '/dashboard/project'}
            className={cn(
              buttonVariants({ variant: 'ghost', size: 'icon', className: 'flex items-center h-8 w-8 rounded-sm' }),
              { 'dark:bg-accent/50 bg-accent': pathname === path }
            )}
          >
            <Icon className='size-5 stroke-1' />
          </Link>
        </TooltipTrigger>
        <TooltipContent side='right'><p>{label}</p></TooltipContent>
      </Tooltip>
    </li>
  );
}

export function Sidebar({ routes }: SidebarProps) {

  return (
    <nav className='flex flex-col gap-1 border-r h-full'>
      <ul>
        {routes.map((group) => (
          <div key={group.label} className='flex flex-col min-w-0 gap-0.5'>
            <div className='flex flex-col w-full p-2 gap-0.5'>
              {group.items?.map((route) => (
                <SibebarItem key={route.label} {...route} />
              ))}
            </div>
            <Separator />
          </div>
        ))}
      </ul>
    </nav>
  );
}