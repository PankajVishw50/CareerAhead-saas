import { forwardRef, useEffect, useRef, useState } from "react";
import { ChatMessageList } from "@/components/ui/chat/chat-message-list";
import { AnimatePresence, motion } from "framer-motion";
import { ChatBubble, ChatBubbleMessage, ChatBubbleTimestamp } from "@/components/ui/chat/chat-bubble";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { ChatInput } from "@/components/ui/chat/chat-input";
import { Button } from "@/components/ui/button";
import {
  CopyIcon,
  CornerDownLeft,
  Mic,
  Paperclip,
  RefreshCcw,
  Volume2,
  Eye,
  EyeOff,
} from "lucide-react";
import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from "@/components/ui/resizable";
import { format } from "date-fns"

import useAuth from "@/hooks/useAuth";
import { urls } from "@/utils/urls";
import { toast } from "@/hooks/use-toast";
import ChatList from "./ChatList";
import useChat from "@/hooks/useChat";
import useWebSocket from "@/hooks/useWebSocket";
import useScreenMode from "@/hooks/useScreenMode";
import { useIsMobile } from "@/hooks/use-mobile";

const ChatBox = ({ chat_id = null }) => {
  const { auth_request, user } = useAuth();
  const { send } = useWebSocket();
  const { count_unseen_messages, update_seen, messages, get_chat } = useChat();
  const { screenMode } = useScreenMode();
  const isMobile = useIsMobile();

  const { fetch_chat, chatsMeta, get_messages, fetch_messages, chats, get_ordered_chat } = useChat();
  const messagesListRef = useRef(null);
  const formRef = useRef(null);
  const inputRef = useRef(null);
  const [input, setInput] = useState("");
  const AllowMsgFetch = useRef(false);
  const [activeChat, setActiveChat] = useState(chat_id);
  const chat_messages = get_messages(activeChat).slice().reverse();
  const chat = get_chat(activeChat);
  const is_chat_active = chat && chat.is_active;


  const msgFetchMetaRef = useRef({
    ...chatsMeta[chat_id]
  });

  // Set activeChat
  useEffect(() => {
    if (activeChat) {
      return;
    }
    setActiveChat(chats[0]?.id);
  }, [chats]);

  // Update Seen of activeChat
  useEffect(() => {
    if (!activeChat || count_unseen_messages(activeChat) <= 0) {
      return;
    }
    update_seen(activeChat, true)
  }, [activeChat, messages]);

  // Message related
  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      handleSendMessage(e);
    }
  };

  // Allow Message fetching if pointer set to 0
  useEffect(() => {
    msgFetchMetaRef.current = {
      ...chatsMeta[chat_id],
    }

    if (chatsMeta[activeChat]?.fetch_counter <= 0 && !chatsMeta[activeChat]?.fetching) {
      AllowMsgFetch.current = true;
    }
  }, [chatsMeta]);


  useEffect(() => {

    const handleEventListener = () => {
      const node = messagesListRef.current;
      if (node.scrollTop > 400 || !AllowMsgFetch.current) {
        return;
      }
      fetch_messages(activeChat);
      AllowMsgFetch.current = false;
    }
    messagesListRef.current?.addEventListener("scroll", handleEventListener);

    return () => {
      messagesListRef.current?.removeEventListener("scroll", handleEventListener);
    }
  }, []);


  const handleSendMessage = (e) => {
    e.preventDefault();
    console.log(e)

    // Send Over websocket

    if (!input || !activeChat) return;

    const _result = send(JSON.stringify({
      type: "message.new",
      payload: {
        chat_id: activeChat,
        message: input,
      }
    }));

    if (!_result) {
      toast({
        description: "failed to send message",
        variant: "destructive",
      });
      return;
    }

    setInput("");
    formRef.current?.reset();
  }

  return (
    <div className="chatbox-root flex flex-1 text-white w-full overflow-y-auto">
      <ResizablePanelGroup
        onLayout={(sizes) => {
          document.cookie = `react-resizable-panels:layout=${JSON.stringify(
            sizes,
          )}`;
        }}
        className="flex-1 items-stretch"
        direction="horizontal"


      >

        <ResizablePanel
          defaultSize={isMobile ? 14 : 30}
          collapsible={true}
          minSize={isMobile ? 0 : 20}
          maxSize={isMobile ? 14 : 30}
        >
          <ChatList activeChat={activeChat} setActiveChat={setActiveChat} isMobile={isMobile} />
        </ResizablePanel>

        <ResizableHandle withHandle />

        <ResizablePanel defaultSize={70} minSize={30}>

          <div className="flex flex-col flex-1 w-full overflow-y-auto bg-muted/40 h-[calc(100svh-64px-theme(spacing.4))]">
            <div className="text-white flex w-full flex-col flex-1 overflow-y-auto">
              <ChatMessageList ref={messagesListRef}>
                <AnimatePresence>
                  {
                    user && chat_messages.map((message, index) => {
                      const variant = message.sender === user.id ? "sent" : "received";

                      return (
                        <motion.div
                          key={index}
                          layout
                          initial={{ opacity: 0, scale: 1, y: 50, x: 0 }}
                          animate={{ opacity: 1, scale: 1, y: 0, x: 0 }}
                          exit={{ opacity: 0, scale: 1, y: 1, x: 0 }}
                          transition={{
                            opacity: { duration: 0.1 },
                            layout: {
                              type: "spring",
                              bounce: 0.3,
                              duration: index * 0.05 + 0.2,
                            },
                          }}
                          style={{ originX: 0.5, originY: 0.5 }}
                          className="flex flex-col gap-2"
                        >
                          <ChatBubble key={index} variant={variant}>
                            <Avatar>
                              <AvatarImage
                                src=""
                                alt="Avatar"
                                className="dark:invert"
                              />
                              <AvatarFallback>
                                🤖
                              </AvatarFallback>
                            </Avatar>

                            <ChatBubbleMessage isLoading={false}>
                              {message.msg}

                              <div className="flex justify-end items-center mt-2 gap-2">

                                <ChatBubbleTimestamp timestamp={format(message.created_at_dt, "hh:mm a")} className="mt-0" />
                                {
                                  variant === "sent" && (
                                    message.seen ? (
                                      <Eye size={14} color="#1d4ed8" />
                                    ) : (
                                      <EyeOff size={14} />
                                    )
                                  )
                                }
                              </div>

                            </ChatBubbleMessage>

                          </ChatBubble>
                        </motion.div>
                      );
                    })
                  }
                </AnimatePresence>
              </ChatMessageList>
            </div>

            <div className="px-4 pb-4 bg-muted/40">
              <form
                ref={formRef}
                onSubmit={handleSendMessage}
                className="relative rounded-lg border bg-background focus-within:ring-1 focus-within:ring-ring"
              >
                <ChatInput
                  ref={inputRef}
                  value={input}
                  onKeyDown={handleKeyDown}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder={is_chat_active ? "Type your message here..." : "Chat is disabled. You are not allowed to send message"}
                  className="min-h-12 resize-none rounded-lg bg-background border-0 p-3 shadow-none focus-visible:ring-0"
                  disabled={!is_chat_active}
                ></ChatInput>
                <div className="flex items-center p-3 pt-0">
                  <Button variant="ghost" size="icon"

                    disabled={!is_chat_active}
                  >
                    <Paperclip className="size-4" />
                    <span className="sr-only">Attach file</span>
                  </Button>

                  <Button variant="ghost" size="icon"
                    disabled={!is_chat_active}
                  >
                    <Mic className="size-4" />
                    <span className="sr-only">Use Microphone</span>
                  </Button>

                  <Button
                    disabled={!is_chat_active}
                    type="submit"
                    size="sm"
                    className="ml-auto gap-1.5"
                  >
                    Send Message
                    <CornerDownLeft className="size-3.5" />
                  </Button>
                </div>
              </form>
            </div>
          </div>
        </ResizablePanel>

      </ResizablePanelGroup>
    </div >
  )
}

export default ChatBox;
