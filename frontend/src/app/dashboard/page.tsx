import { Menu } from "./components/menu";
import { Header } from "./components/header";
import { Content } from "./components/content";

export default function DashboardPage() {
  return (
    <div className="flex flex-row w-screen min-h-screen">
      <Menu />
      <section className="bg-primary-foreground flex flex-col w-full ps-24">
        <Header />
        <Content />
      </section>
    </div>
  );
}
