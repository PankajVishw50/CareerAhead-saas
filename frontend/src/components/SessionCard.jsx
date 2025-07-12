import { Card } from "@/components/ui/card"
import {
  Avatar,
  AvatarImage,
  AvatarFallback
} from "@/components/ui/avatar"
import { Button } from "./ui/button";
import { NavLink } from "react-router";
import { format } from "date-fns";
import { cn } from "@/lib/utils";

const SessionCard = ({ session = {} }) => {
  return (
    <Card
      className={cn(
        "p-3 m-1 flex justify-between gap-2",
        // "border-r-0 border-l-0 border-t-0 rounded-b-none",
        "max-w-full",
        "flex-1 w-full",
      )}
      key={session.id}
    >
      <Avatar size={40} className="h-16 w-16">
        <AvatarImage src={session.user.image} size={32} />
        <AvatarFallback>
          AN
        </AvatarFallback>
      </Avatar>
      <div className="flex flex-1 flex-col gap-0 w-full">
        <h4 className="text-md">{session.user.name}</h4>
        <div className="text-sm">{format(session.from_datetime, "h:mm a")} - {format(session.to_datetime, "h:mm a")}</div>
        <div className="text-sm">{session.fee} ₹</div>
        <div className="text-[.6rem] text-right">{format(session.from_datetime, "h a MMM d, yyyy")} To {format(session.to_datetime, "h a MMM d, yyyy")}</div>
      </div>
      <div className="flex items-end">
        <Button asChild>
          <NavLink to={"/chat"}>
            Chat
          </NavLink>
        </Button>
      </div>
    </Card>
  )
}

export default SessionCard
