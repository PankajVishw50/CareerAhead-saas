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
import { Tooltip, TooltipContent, TooltipTrigger } from "./ui/tooltip";
import { capitalize } from "@/utils/helpers";
import { useNavigate } from "react-router";

const SessionCard = ({ session = {} }) => {
  const navigate = useNavigate();

  return (
    <Tooltip>
      <TooltipTrigger className="w-full">
        <NavLink to="/chat">
          <Card
            className={cn(
              "p-3 m-1 flex gap-2",
              "max-w-full",
              "flex-1 w-full",

              session.type === "active" && "bg-gradient-to-r from-[#e63946]/30 via-white/20 to-[#fbc6c9]/20",
              session.type === "active" &&
              "hover:bg-gradient-to-r hover:from-[#e63946]/50 hover:via-white/40 hover:to-[#fbc6c9]/40",

              session.type === "upcoming" &&
              "bg-gradient-to-r from-[#4895ef]/30 via-white/20 to-[#a8d2ff]/20",
              session.type === "upcoming" &&
              "hover:bg-gradient-to-r hover:from-[#4895ef]/50 hover:via-white/40 hover:to-[#a8d2ff]/40",
              "transition-all",

              "hover:scale-[1.02]",
            )}
            key={session.id}
          >
            <Avatar size={40} className="h-16 w-16">
              <AvatarImage src={session.user.image} size={32} />
              <AvatarFallback>
                AN
              </AvatarFallback>
            </Avatar>
            <div className="flex flex-1 flex-col gap-0 w-full justify-start items-start">
              <h4 className="text-md">{capitalize(session.user.name)}</h4>
              <div className="text-sm">{format(session.from_datetime, "h:mm a")} - {format(session.to_datetime, "h:mm a")}</div>
              <div className="text-sm">{session.fee} ₹</div>
              <div className="text-[.6rem] text-right">{format(session.from_datetime, "h a MMM d, yyyy")} To {format(session.to_datetime, "h a MMM d, yyyy")}</div>
            </div>
            <div className="flex items-end">
              <Button onClick={() => navigate("/chat")} asChild >
                <span>Chat</span>
              </Button>
            </div>
          </Card>
        </NavLink>
      </TooltipTrigger>

      <TooltipContent>
        {
          capitalize(session.type)
        } Session
      </TooltipContent>
    </Tooltip>
  )
}

export default SessionCard
