import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { toast } from "@/hooks/use-toast";
import {
  Avatar,
  AvatarImage,
  AvatarFallback
} from "@/components/ui/avatar"
import { format } from "date-fns"

import useAuth from "@/hooks/useAuth";
import { get_param_url } from "@/utils/collections";
import { urls } from "@/utils/urls";
import { useEffect, useRef, useState } from "react";
import ProfileUser from "@/assets/images/dummycounsellor.jpg"
import { Button } from "./ui/button";
import { cn } from "@/lib/utils";
import { NavLink } from "react-router";
import { MoveRight, ArrowRight } from "lucide-react";
import { Badge } from "@/components/ui/badge"
import { capitalize } from "@/utils/helpers";

const MAX_RETRIES = 3;

const SessionsWindow = ({
  type = "active",
  background_color = "bg-[#c8b6ff]/10",
  hover_background_color = "hover:bg-[#c8b6ff]/20"
}) => {

  const { auth_request } = useAuth();

  const [isHovered, setIsHovered] = useState(false);
  const [sessions, setSessions] = useState([]);
  const [retries, setRetries] = useState(MAX_RETRIES);
  const [nextFetchUrl, setNextFetchUrl] = useState(get_param_url(urls.sessions.get_url(), { type }));
  const fetching = useRef(false)

  useEffect(() => {
    if (!nextFetchUrl || retries <= 0) {
      return;
    }

    fetch_sessions();

  }, [nextFetchUrl, retries])

  const fetch_sessions = async () => {
    if (fetching.current) {
      return;
    }
    fetching.current = true
    setRetries(prev => prev - 1)
    console.log("fetching sessions")

    const { json, error } = await auth_request(
      nextFetchUrl,
      {
        method: "GET"
      }
    );
    fetching.current = false;

    if (error) {
      console.warn("failed to fetch sessions of types: ", type);
      return;
    }

    setRetries(MAX_RETRIES)
    setSessions(prev => [...prev, ...json.items]);
    setNextFetchUrl(json.next_url);
  }

  // return <CardTest />


  return (
    <Card
      className={
        cn(
          "w-full max-w-md p-0 p-0 z-20 overflow-hidden flex flex-col justify-end",
          // "border-4"
        )
      }
      style={{
        // "border-color": border_color,
      }}
    >
      <CardContent className="p-0 flex flex-1 flex-col">

        {sessions.slice(0, 5).map((session, index) => {
          return (
            <Card
              className={cn(
                "p-3 flex gap-2",
                "border-r-0 border-l-0 border-t-0 rounded-b-none"
              )}
              key={session.id}>
              <Avatar size={40} className="h-16 w-16">
                <AvatarImage src={session.user.image} size={32} />
                <AvatarFallback>
                  AN
                </AvatarFallback>
              </Avatar>
              <div className="flex flex-col gap-0 max-w-md w-full">
                <h4 className="text-md">{session.user.name}</h4>
                <div className="text-sm">{format(session.from_datetime, "h:mm a")} - {format(session.to_datetime, "h:mm a")}</div>
                <div className="text-sm">{session.fee} ₹</div>
                <div className="text-[.6rem] text-right">{format(session.from_datetime, "h a MMM d, yyyy")} To {format(session.to_datetime, "h a MMM d, yyyy")}</div>
              </div>
              <div className="flex-1 flex items-end">
                <Button asChild>
                  <NavLink to={"/chat"}>
                    Chat
                  </NavLink>
                </Button>
              </div>
            </Card>
          )
        })}

        {sessions.length == 0 && (
          <div className="flex-1 flex justify-center items-center h-full">
            No {capitalize(type)} Session Found
          </div>

        )}

      </CardContent>
      <CardFooter
        onMouseEnter={() => {
          setIsHovered(true);
        }}
        onMouseLeave={() => {
          setIsHovered(false);
        }}

        className={
          cn(
            "h-14 flex w-full items-center justify-center p-0",
            // "p-5",


            // "bg-[#c8b6ff]/10 hover:bg-[#c8b6ff]/20",
            background_color, hover_background_color,
            "transition-colors duration-500 ease-in-out"
          )
        }
      >
        {
          isHovered ?
            (
              <NavLink to="/chat" className="flex gap-2 justify-center items-center flex-1 h-full">
                <span>
                  See All
                </span>
                <ArrowRight size={18} />

              </NavLink>
            ) : (
              <Badge variant="ghost" className=" m-5 border-white/25 flex  gap-2 justify-center w-full text-sm py-2">
                {capitalize(type)} Chats

                {
                  sessions.length > 0 && (
                    <Badge variant="destructive" className="rounded-full h-6 w-6 flex justify-center tabular-nums text-xs">
                      {sessions.length}
                    </Badge>
                  )
                }
              </Badge>
            )

        }
      </CardFooter>

    </Card >
  )
}

export default SessionsWindow
