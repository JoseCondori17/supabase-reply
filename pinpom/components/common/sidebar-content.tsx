import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { buttonVariants } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import type { Route } from "@/constants/route";
import Link from "next/link";
import React from "react";

interface SidebarContentProps {
  title: string;
  items: Route[];
};

function SidebarContentItem({ label, path }: Route) {
  return (
    <Link
      href={path ?? '/dashboard/project'}
      className={cn(
        buttonVariants({
          variant: 'ghost',
          size: 'sm',
          className: 'flex items-center justify-start h-[24px] text-[0.8rem] text-start font-light text-muted-foreground rounded-sm hover:font-normal hover:bg-transparent'
        }),
      )}
    >{label}</Link>
  );
}

export function SidebarContent({ title, items }: SidebarContentProps) {
  return (
    <ScrollArea className='w-70 border-r h-full'>
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
                    <SidebarContentItem key={subitem.label} label={subitem.label} path={subitem.path} />
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