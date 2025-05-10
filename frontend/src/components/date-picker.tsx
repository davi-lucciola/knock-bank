"use client";

import { useState } from "react";
import { format } from "date-fns";
import { Calendar as CalendarIcon } from "lucide-react";

import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { ptBR } from "date-fns/locale";
import { Matcher } from "react-day-picker";

type DatePickerProps = {
  date: string | Date;
  disableDays?: Matcher | Matcher[];
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  onChange: (...event: any[]) => void;
};

function getLastHundredYears() {
  const lastHundredYears = [];
  const currentYear = new Date().getFullYear();

  for (let year = currentYear; year >= currentYear - 100; year--) {
    lastHundredYears.push(year);
  }
  return lastHundredYears;
}

export function DatePicker({
  date: dateProp,
  disableDays,
  onChange,
}: DatePickerProps) {
  const [isOpen, setIsOpen] = useState(false);
  const date = typeof dateProp == "string" ? new Date(dateProp) : dateProp;
  const [displayedMounth, setDisplayedMounth] = useState<Date>(
    !date ? new Date() : new Date(date.getFullYear(), date.getMonth())
  );

  return (
    <Popover open={isOpen} onOpenChange={setIsOpen}>
      <PopoverTrigger asChild>
        <Button
          variant={"outline"}
          className={cn(
            "justify-start text-left font-normal",
            !date && "text-muted-foreground"
          )}
        >
          <CalendarIcon />
          {date ? format(date, "dd/MM/yyyy") : <span>Escolha uma Data</span>}
        </Button>
      </PopoverTrigger>
      <PopoverContent className="flex w-auto flex-col space-y-2 p-2">
        <Select
          value={`${displayedMounth.getFullYear()}`}
          onValueChange={(value: string) =>
            setDisplayedMounth(
              new Date(Number(value), displayedMounth.getMonth())
            )
          }
        >
          <SelectTrigger className="w-full hover:co">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectGroup>
              {getLastHundredYears().map((year, index) => (
                <SelectItem key={index} value={`${year}`}>
                  {year}
                </SelectItem>
              ))}
            </SelectGroup>
          </SelectContent>
        </Select>
        <div className="rounded-md border">
          <Calendar
            mode="single"
            locale={ptBR}
            selected={date}
            onSelect={(event) => {
              onChange(event);
              setIsOpen(false);
            }}
            disabled={disableDays}
            initialFocus
            month={displayedMounth}
            onMonthChange={(mounth) => setDisplayedMounth(mounth)}
          />
        </div>
      </PopoverContent>
    </Popover>
  );
}
