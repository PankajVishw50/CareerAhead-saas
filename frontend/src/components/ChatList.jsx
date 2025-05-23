import { toast } from "@/hooks/use-toast";
import useAuth from "@/hooks/useAuth";
import useChat from "@/hooks/useChat";
import { get_param_url } from "@/utils/collections";
import { urls } from "@/utils/urls";
import { useEffect, useState } from "react";
import ChatSidebar from "./ChatSidebar";

const ChatList = ({ activeChat, setActiveChat, isMobile }) => {
  const { chats } = useChat();

  return (
    <div>
      <ChatSidebar chats={chats} activeChat={activeChat} setActiveChat={setActiveChat} isCollapsed={isMobile} isMobile={isMobile} />
    </div>
  )
}

export default ChatList
