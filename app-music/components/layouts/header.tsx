import Image from "next/image";
import Link from "next/link";
import brandPinPom from "@/public/image/logo.png";

import { routes } from "@/constants/route";
import { Button } from "@/components/ui/button";

function Navbar() {
  return (
    <div className="flex items-center gap-8">
      <Link href="/">
        <Image
          src={brandPinPom}
          width={100}
          height={70}
          alt="Brand"
        />
      </Link>
      <nav className="flex">
        <ul className="flex items-center justify-center gap-4">
          {routes.map((item, idx) => (
            <li key={idx}>
              <Link href={item.href}>{item.label}</Link>
            </li>
          ))}
        </ul>
      </nav>
    </div>
  );
}

export function Header() {
  return (
    <header className="container mx-auto py-2 md:px-24">
      <div className="flex justify-between items-center">
        <Navbar />
        <div>
          <Button size="sm">Subscribe</Button>
        </div>
      </div>
    </header>
  );
}