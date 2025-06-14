'use client'
import { buttonVariants } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import type { Route } from "@/constants/route";
import { cn } from "@/lib/utils";
import Link from "next/link";
import { usePathname } from "next/navigation";
import React from "react";

interface SidebarContentProps {
  title: string;
  items: Route[];
};

function SidebarContentItem({ label, url }: Route) {
  const pathname = usePathname();
  return (
    <Link
      href={url ?? '/dashboard/project'}
      className={cn(
        buttonVariants({
          variant: 'ghost',
          size: 'sm',
          className: cn(
            'flex items-center justify-start h-[24px] text-[0.8rem] text-start text-muted-foreground rounded-sm hover:font-normal hover:bg-transparent',
            { 'font-normal text-black': pathname.includes(url) },
            { 'font-light': !pathname.includes(url) }
          )
        }),
      )}
    >{label}</Link>
  );
}

export function SidebarContent({ title, items }: SidebarContentProps) {
  return (
    <ScrollArea className='w-[250px] border-r h-full'>
      <div className='px-6 py-2.5 font-medium'>
        {title}
      </div>
      <Separator />
      <ul className="space-y-0">
        {items.map((item, index) => (
          <React.Fragment key={item.label}>
            <li>
              <div className="px-3 py-4 space-y-1">
                <p className="text-[0.8rem] text-muted-foreground uppercase px-3 py-1.5">{item.label}</p>
                <div>
                  {item.items?.map((subitem) => (
                    <SidebarContentItem key={subitem.label} label={subitem.label} url={subitem.url} />
                  ))}
                </div>
              </div>
            </li>
            {index < items.length - 1 && <Separator className="my-2" />}
          </React.Fragment>
        ))}
      </ul>
    </ScrollArea>
  );
}