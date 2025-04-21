import { useEffect, useState } from "react";

import useAuth from "@/hooks/useAuth";
import {urls} from "@/utils/urls";
import {get_param_url} from "@/utils/collections";
import { date_formatted, datetime_formatted, timezone_formatted } from "@/utils/date";
import { format } from "date-fns";
import { ChevronRight, ChevronLeft } from "lucide-react"

import { Check } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { CalendarIcon } from "lucide-react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Calendar } from "@/components/ui/calendar"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"
import { toast } from "@/hooks/use-toast";
import Spinner from "./ui/Spinner";

const CounsellorScheduleWindow = ({counsellor}) => {
  const {auth_request} = useAuth();

  const [selectedId, setSelectedId] = useState(null);
  const [slots, setSlots] = useState({});
  const [today] = useState(new Date());
  const [date, setDate] = useState(today);
  const [booking, setBooking] = useState(false);

  useEffect(() => {
    fetch_slots(date);
    setSelectedId(null);
  }, [date]);

  const _fetch_slots = async (dates, timezone) => {
    const {json, error} = await auth_request(
      get_param_url(urls.available_slots.get_url(counsellor.id), {dates: dates, timezone: timezone}),
      {
        method: "GET",
      }
    )
    if (error) {
      toast({
        description: "Failed to fetch slots",
        variant: "destructive"
      })
      return false;
    }

    // Save to slots
    const slots_batch = {}
    for (const date in json) {
      slots_batch[date] = json[date];
    }
    setSlots(prev => {
      return {
        ...prev,
        ...slots_batch,
      }
    });
    return true;
  }

  const fetch_slots = async (date) => {
    // if date is today use stored date
    if (date_formatted(date) == date_formatted(today)) {
      date = today;
    }

    // Check if date is already fetched
    if (slots[date_formatted(date)]) {
      return false;
    }

    const dates = []
    const timezone = timezone_formatted();

    // Get current and 5 days ahead
    for (let i = 0; i <= 5; i++) {
      const new_date = new Date(date);
      new_date.setDate(new_date.getDate() + i);
      const new_date_formatted = date_formatted(new_date);

      // Ignore If already fetched
      if (slots[new_date_formatted]) {
        continue;
      }

      // Check if date is today
      // In which case we need to pass datetime
      // otherwise date only
      if (new_date_formatted === date_formatted()){
        dates.push(datetime_formatted(new_date))
      } else {
        dates.push(date_formatted(new_date));
      }
    }

    // Fetch
    _fetch_slots(dates, timezone);
  }

  const get_slots = (date) => {
    // Check if date is today
    let formatted_date = null;
    if (date_formatted(date) == date_formatted(today)) {
      formatted_date = datetime_formatted(today);
    } else {
      formatted_date = date_formatted(date);
    }

    return slots[formatted_date] || [];
  }


  const book_slot = async () => {
    // Check if there is slot
    let d = date_formatted(date)
    if (date_formatted(date) == date_formatted(today)) {
      d = datetime_formatted(date)
    }
    const slot = slots[d]?.find((s) => s.id === selectedId)

    if (!slot){
      return toast({
        description: "select valid slot",
        variant: "destructive",
      })
    }

    setBooking(true);
    // Fetch
    const {json, error} = await auth_request(
      urls.session.get_url(counsellor.id, slot.id),
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          from_datetime: slot.from_datetime,
        })
      }
    )
    setBooking(false);

    if (error){
      return toast({
        description: "Failed to book slot",
        variant: "destructive",
      })
    }

    toast({
      description: "Successfully Booked slot",
    });

    setSlots(prev => {
      return {
        ...prev,
        [d]:[],
      }
    })
    fetch_slots(date);
    setSelectedId(null);

  }


  return (
      <div className="w-full h-full">
        <div className="flex gap-2">
          <Button variant="outline" size="icon"
          onClick={() => {
            const d = new Date(date);
            d.setDate(d.getDate() - 1);
            setDate(d);
          }}
          disabled={date_formatted(date) == date_formatted(today)}
          >
            <ChevronLeft />
          </Button>

          <Popover>
            <PopoverTrigger asChild>
              <Button
                variant={"outline"}
                className={cn(
                  "w-[240px] justify-start text-left font-normal",
                  !date && "text-muted-foreground"
                )}
              >
                <CalendarIcon />
                {/* {date ? format(date, "PPP") : <span>Pick a date</span>} */}
                {date_formatted(date)}
              </Button>
            </PopoverTrigger>
            <PopoverContent className="w-auto p-0" align="start">
              <Calendar
                mode="single"
                selected={date}
                onSelect={setDate}
                disabled={(date) => date < new Date((new Date()).setHours(0, 0, 0, 0))} // Disabled Past days
                initialFocus
              />
            </PopoverContent>
          </Popover>

          <Button variant="outline" size="icon"
          onClick={() => {
            const d = new Date(date);
            d.setDate(d.getDate() + 1);
            setDate(d);
          }}
          >
            <ChevronRight />
          </Button>

        </div>

        <div>
          <div className="flex gap-4 p-4 flex-wrap justify-center">
            {get_slots(date) ? get_slots(date).map((slot) => {
              const isSelected = selectedId === slot.id;

              return (
                <Card
                  key={slot.id}
                  onClick={() => setSelectedId(slot.id)}
                  className={cn(
                    "cursor-pointer transition-shadow hover:shadow-lg border-2 max-w-xs",
                    isSelected ? "border-blue-500 bg-gray-900" : "border-gray-200"
                  )}
                >
                  <CardContent className="p-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-lg font-semibold">
                          {format(slot.from_datetime, "hh:mm a")} - {format(slot.to_datetime, "hh:mm a")} ({slot.duration.slice(0,5)} hrs)
                        </p>
                        <p className="text-sm text-green-500">Fee: ₹{slot.fee}</p>
                        {/* <p className="text-sm text-gray-400">Timezone: {slot.timezone}</p> */}
                      </div>
                      {/* {isSelected && <Check className="text-blue-500 w-5 h-5" />} */}
                    </div>
                  </CardContent>
                </Card>
              );
            })
            : <div className="text-white">No Slots Available</div>
          }
          </div>

          <div className="flex justify-end mt-6">
            <Button
            disabled={selectedId === null || booking}
            onClick={book_slot}
            >
              {
                booking ? <Spinner spinning={booking}/>
                : "Schedule"
              }

            </Button>
          </div>

        </div>
      </div>
  )
}

export default CounsellorScheduleWindow;
