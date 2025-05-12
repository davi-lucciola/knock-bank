import { SquaresFour } from "@phosphor-icons/react";
import { AuthService } from "@/modules/auth/auth.service";
import { KnockBankLogo } from "@/components/knock-bank-logo";
import { LogoutButton } from "@/modules/auth/components/logout-button";

type MenuProps = {
  authService: AuthService;
};

export function Menu({ authService }: MenuProps) {
  return (
    <aside className="w-24 bg-neutral-800 h-screen flex flex-col justify-around items-center py-4 fixed left-0">
      <KnockBankLogo size={64} />
      <nav className="flex-1 mt-16">
        <ul className="flex flex-col gap-8">
          <li>
            <SquaresFour size={32} className="fill-primary" />
          </li>
          {/* <li>
            <MyAccount account={account} />
          </li> */}
        </ul>
      </nav>
      <LogoutButton authService={authService} />
    </aside>
  );
}
