import Image from "next/image";

type LogoProps = {
  size: number;
};

export function KnockBankLogo({ size }: LogoProps) {
  return (
    <Image
      src="/knockbank-logo.svg"
      alt="knockbank-logo"
      width={size}
      height={size}
    />
  );
}
