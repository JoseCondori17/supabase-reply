import { Button } from "@/components/ui/button";
import { Code, HelpCircleIcon, InboxIcon } from "lucide-react";

export function Navbar() {
  return (
    <div className='flex justify-between p-2.5 border-b'>
      <div className='flex items-center gap-x-2'>
        <Code className='size-3.5' />
      </div>
      <div className="flex items-center gap-x-2">
        <Button size='sm' variant='outline' className='text-xs h-[26px] rounded-sm'>
          Feedback
        </Button>
        <Button size='icon' variant='ghost' className='text-xs h-[26px] w-7 rounded-sm'>
          <InboxIcon className='size-3.5 stroke-1' />
        </Button>
        <Button size='icon' variant='ghost' className='text-xs h-[26px] w-7 rounded-sm'>
          <HelpCircleIcon className='size-3.5 stroke-1' />
        </Button>
      </div>
    </div>
  );
}