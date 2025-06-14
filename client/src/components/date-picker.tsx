"use client";

import { useState } from "react";
import { format, addMinutes } from "date-fns";
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
  disabled?: boolean;
};

function getLastHundredYears() {
  const lastHundredYears = [];
  const currentYear = new Date().getFullYear();

  for (let year = currentYear; year >= currentYear - 100; year--) {
    lastHundredYears.push(year);
  }
  return lastHundredYears;
}

function castDateToDisplay(dateToDisplay?: string | Date) {
  if (dateToDisplay && typeof dateToDisplay == "string") {
    const timezoneOffset = new Date().getTimezoneOffset();
    return addMinutes(new Date(dateToDisplay), timezoneOffset);
  } else if (dateToDisplay instanceof Date) {
    return dateToDisplay;
  }
}

export function DatePicker({
  date,
  disableDays,
  onChange,
  disabled = false,
}: DatePickerProps) {
  const [isOpen, setIsOpen] = useState(false);
  const dateToDisplay = castDateToDisplay(date);
  const [displayedMounth, setDisplayedMounth] = useState<Date>(
    !dateToDisplay
      ? new Date()
      : new Date(dateToDisplay.getFullYear(), dateToDisplay.getMonth())
  );

  return (
    <Popover open={isOpen} onOpenChange={setIsOpen}>
      <PopoverTrigger asChild>
        <Button
          disabled={disabled}
          variant={"outline"}
          className={cn(
            "justify-start text-left font-normal",
            !dateToDisplay && "text-muted-foreground"
          )}
        >
          <CalendarIcon />
          {dateToDisplay ? (
            format(dateToDisplay, "dd/MM/yyyy")
          ) : (
            <span>Escolha uma Data</span>
          )}
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
            selected={dateToDisplay}
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
