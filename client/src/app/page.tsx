import { KnockBankLogo } from "@/components/knock-bank-logo";
import { LoginForm } from "@/modules/auth/components/login-form";
import { CreateAccountForm } from "@/modules/account/components/create-account-form";

export default function HomePage() {
  return (
    <div className="bg-white h-screen flex flex-col">
      <Header />
      <Hero />
    </div>
  );
}

function Header() {
  return (
    <header className="container m-auto flex justify-between items-center py-4">
      <div id="logo" className="flex items-center gap-4 text-2xl font-bold">
        <KnockBankLogo size={64} />
        <span> KnockBank</span>
      </div>
      <LoginForm />
    </header>
  );
}

function Hero() {
  return (
    <main className="container m-auto flex flex-col flex-grow justify-center gap-8">
      <h1 className="text-5xl font-extrabold lg:max-w-lg">
        Sempre dando um <strong>Knock Out</strong> nas suas dívidas
      </h1>
      <p className="text-justify text-2xl lg:max-w-lg">
        Venha com o banco que traz a maior facilidade para trânsferências.
        Quando você vê, o dinheiro já está batendo na sua porta.
      </p>
      <CreateAccountForm />
    </main>
  );
}
