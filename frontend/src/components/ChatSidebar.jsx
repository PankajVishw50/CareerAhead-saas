import { cn } from "@/lib/utils";
import { NavLink } from "react-router";
import { buttonVariants } from "./ui/button";
import { MoreHorizontal, SquarePen } from "lucide-react";
import { Avatar, AvatarImage } from "./ui/avatar";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
  TooltipProvider,
} from "@/components/ui/tooltip";


import dummyCounsellorImage from "@/assets/images/dummycounsellor.jpg"
import useChat from "@/hooks/useChat";
import { Badge } from "@/components/ui/badge";


const ChatSidebar = ({ chats, activeChat, setActiveChat, isCollapsed, isMobile }) => {
  const { get_messages, count_unseen_messages } = useChat();

  return (
    <div
      data-collapsed={isCollapsed}
      // data-mobile={isMobile}
      className="relative group flex flex-col h-full bg-muted/10 dark:bg-muted/20 gap-4 p-2 data-[collapsed=true]:p-2 "
    >
      {!isCollapsed && (
        <div className="flex justify-between p-2 items-center">
          <div className="flex gap-2 items-center text-2xl">
            <p className="font-medium">Chats</p>
            <span className="text-zinc-300">({chats.length})</span>
          </div>

          <div>
            <NavLink
              to="#"
              className={cn(
                buttonVariants({ variant: "ghost", size: "icon" }),
                "h-9 w-9",
              )}
            >
              <MoreHorizontal size={20} />
            </NavLink>

            <NavLink
              to="#"
              className={cn(
                buttonVariants({ variant: "ghost", size: "icon" }),
                "h-9 w-9",
              )}
            >
              <SquarePen size={20} />
            </NavLink>
          </div>
        </div>
      )}

      <nav className="grid gap-1 px-2 group-[[data-collapsed=true]]:justify-center group-[[data-collapsed=true]]:px-2">
        {chats.map((chat, index) => {
          const messages = get_messages(chat.id);
          const unseen_counter = count_unseen_messages(chat.id);

          // Setting this because this var is needed
          chat["variant"] = chat.is_active ? "default" : "secondary"

          return (
            <div
              key={chat.id}
              data-id={chat.id}
              onClick={(e) => {
                setActiveChat(e.currentTarget.dataset.id)
              }}
            >
              {
                isCollapsed ? (
                  <TooltipProvider
                    key={index}
                    data-id={chat.id}
                    className={
                      cn(
                        !chat.is_active ? "bg-zinc-100 hover:bg-zinc-700" : "",
                        activeChat === chat.id ? "bg-blue-500 hover:bg-blue-700" : ""
                      )
                    }
                  >
                    <Tooltip key={index} delayDuration={0}>
                      <TooltipTrigger asChild>
                        <NavLink
                          to="#"
                          className={cn(
                            buttonVariants({ variant: chat.variant, size: "icon" }),
                            "h-11 w-11 md:h-16 md:w-16",
                            activeChat !== chat.id && chat.variant === "secondary" &&
                            "dark:bg-muted dark:text-muted-foreground dark:hover:bg-muted dark:hover:text-white",
                            activeChat === chat.id ? "bg-blue-500 hover:bg-blue-700" : "",
                            "relative",
                          )}
                        >
                          <Avatar className="flex justify-center items-center">
                            <AvatarImage
                              src={dummyCounsellorImage}
                              alt={dummyCounsellorImage}
                              width={6}
                              height={6}
                              className="w-10 h-10 "
                            />
                          </Avatar>{" "}
                          {
                            unseen_counter > 0 && (
                              <Badge
                                className="absolute right-0 top-0 h-4 w-4 rounded-full px-1 font-mono tabular-nums flex justify-center"
                                variant="destructive"
                              >
                                {unseen_counter}
                              </Badge>
                            )
                          }
                          <span className="sr-only">{chat.id}</span>
                        </NavLink>
                      </TooltipTrigger>
                      <TooltipContent
                        side="right"
                        className="flex items-center gap-4 text-black"
                      >
                        {chat.id}
                      </TooltipContent>
                    </Tooltip>
                  </TooltipProvider>
                ) : (

                  <NavLink
                    key={index}
                    to="#"
                    className={cn(
                      buttonVariants({ variant: chat.variant, size: "xl" }),
                      chat.variant === "secondary" &&
                      "dark:bg-muted dark:text-white dark:hover:bg-muted dark:hover:text-white shrink",
                      "justify-start gap-4 w-full",
                      !chat.is_active ? "bg-zinc-500 hover:bg-zinc-700" : "",
                      activeChat === chat.id ? "bg-blue-500 hover:bg-blue-700" : "",
                      "p-2",
                    )}
                  >
                    <Avatar className="flex justify-center items-center">
                      <AvatarImage
                        src={dummyCounsellorImage}
                        alt={dummyCounsellorImage}
                        width={6}
                        height={6}
                        className="w-10 h-10 "
                      />
                    </Avatar>
                    <div className="flex flex-col max-w-28">
                      <span className="truncate">{chat.id}</span>
                      {messages?.length > 0 && (
                        <div className="flex justify-between">
                          <span className="text-zinc-300 text-xs truncate">
                            {/* {messages[messages.length - 1].name.split(" ")[0]} */}
                            {/* :{" "} */}
                            {messages[0].isLoading
                              ? "Typing..."
                              : messages[0].msg}
                          </span>
                          {
                            unseen_counter > 0 && (
                              <Badge
                                className="h-5 w-5 rounded-full px-1 font-mono tabular-nums flex justify-center"
                                variant="destructive"
                              >
                                {unseen_counter}
                              </Badge>
                            )
                          }
                        </div>
                      )}
                    </div>
                  </NavLink>
                )}
            </div>
          )
        })}

      </nav >
    </div >
  );
}

export default ChatSidebar
