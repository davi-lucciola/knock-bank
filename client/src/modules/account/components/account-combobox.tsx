"use client";

import { Button } from "@/components/ui/button";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { useAccounts } from "../hooks/use-accounts";

type AccountsComboboxProps = {
  accountId: number;
  setAccountId: (accountId: number) => void;
};

export function AccountCombobox({
  accountId,
  setAccountId,
}: AccountsComboboxProps) {
  const { accounts, filters, setFilters, buttonLabel, popover } =
    useAccounts(accountId);

  return (
    <Popover open={popover.isOpen} onOpenChange={popover.setIsOpen}>
      <PopoverTrigger asChild>
        <Button variant="outline" className="w-full">
          {buttonLabel}
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[462px]">
        <Command className="w-full" shouldFilter={false}>
          <CommandInput
            placeholder="Pesquise uma conta..."
            value={filters.search}
            onValueChange={(value) => setFilters({ search: value })}
          />
          <CommandList>
            <CommandEmpty>Não há resultados para mostrar.</CommandEmpty>
            <CommandGroup>
              {accounts?.data.map((account) => (
                <CommandItem
                  key={account.id}
                  className="flex flex-col items-start cursor-pointer"
                  onSelect={() => {
                    setAccountId(account.id);
                    popover.setIsOpen(false);
                  }}
                >
                  <p>{account.person.name}</p>
                  <small className="font-bold">{account.person.cpf}</small>
                </CommandItem>
              ))}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  );
}
