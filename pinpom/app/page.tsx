import { Button } from "@/components/ui/button";
import Image from "next/image";
import Link from "next/link";
import LogoPinPom from "../public/image/logo.png";

export default function Home() {
  return (
    <div className="flex flex-col">
      <header className="container mx-auto py-4">
        <div className="flex items-center justify-between">
          <Image src={LogoPinPom} width={110} height={45} alt="Logo of Page" />
          <div className="flex items-center gap-x-2">
            <Button size="sm" variant="outline" className="text-xs">Login</Button>
            <Button size="sm" className="text-xs" asChild>
              <Link href="/dashboard/project/u7shjn23urfas/sql">Get Started</Link>
            </Button>
          </div>
        </div>
      </header>
      <main></main>

    </div>
  );
}
