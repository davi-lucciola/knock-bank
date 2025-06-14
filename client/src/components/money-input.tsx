import { ComponentProps, forwardRef } from "react";
import { Input } from "./ui/input";
import { formatBrasilianReal, toBrasilianReal } from "@/lib/masks";

export const MoneyInput = forwardRef<HTMLInputElement, ComponentProps<"input">>(
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  ({ className, value, onChange, ...props }, ref) => {
    return (
      <Input
        type="text"
        placeholder="R$ 10,00"
        ref={ref}
        value={formatBrasilianReal(toBrasilianReal((value as number) ?? 0)!)}
        onChange={(event) => {
          const { value } = event.target;
          event.target.value = formatBrasilianReal(value);

          if (onChange) {
            onChange(event);
          }
        }}
        {...props}
      />
    );
  }
);
MoneyInput.displayName = "Money Input";
