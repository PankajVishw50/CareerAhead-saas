import { forwardRef, useEffect, useRef, useState } from "react";
import { ChatMessageList } from "@/components/ui/chat/chat-message-list";
import { AnimatePresence, motion } from "framer-motion";
import { ChatBubble, ChatBubbleMessage } from "@/components/ui/chat/chat-bubble";
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
} from "lucide-react";
import useAuth from "@/hooks/useAuth";
import { urls } from "@/utils/urls";
import { toast } from "@/hooks/use-toast";

const Messages = [
  { message: "Hi! How are you doing?", variant: "received" },
  { message: "Hey, I'm doing great! How about you?", variant: "sent" },
  { message: "I'm good too. What can you do?", variant: "received" },
  { message: "I can help you with coding, questions, or just chat.", variant: "sent" },
  { message: "That’s cool. Can you write a Python function for me?", variant: "received" },
  { message: "Sure! What should the function do?", variant: "sent" },
  { message: "I want a function that checks if a number is prime.", variant: "received" },
  { message: "Got it. Here's a simple implementation.", variant: "sent" },
  { message: "Thanks! That was quick.", variant: "received" },
  { message: "You're welcome 😊 Anything else?", variant: "sent" },
  { message: "Can you also explain how it works?", variant: "received" },
  { message: "Of course. It loops through numbers and checks for divisibility.", variant: "sent" },
  { message: "Nice. Do you know React too?", variant: "received" },
  { message: "Yes, I can help you with React components, hooks, and more.", variant: "sent" },
  { message: "What is a ref in React?", variant: "received" },
  { message: "A ref gives direct access to a DOM element or a React element.", variant: "sent" },
  { message: "Ah, that makes sense now.", variant: "received" },
  { message: "Great! Happy to help.", variant: "sent" },
  { message: "I'll reach out if I need more help.", variant: "received" },
  { message: "Anytime! Have a productive day! 🚀", variant: "sent" }
];

const ChatBox = ({ chat_id }, ref) => {
  const { auth_request, user } = useAuth();

  const messagesListRef = useRef(null);
  const formRef = useRef(null);
  const inputRef = useRef(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const [chat, setChat] = useState(null);
  const [msgFetchCounter, setMsgFetchCounter] = useState(3);
  const [baseMsgURL, _] = useState(urls.messages.get_url(chat_id));
  const [nextMsgURL, setNextMsgURL] = useState(baseMsgURL);
  const msgFetchCounterRef = useRef(msgFetchCounter);

  // TODO: /apt/chats/:chat_id is not implemented yet
  //
  // useEffect(() => {
  //   // Fetch Chat details
  //   (async () => {
  //     const { json, error } = await auth_request(
  //       urls.chat.get_url(chat_id),
  //     )
  //
  //     if (error) {
  //       toast({
  //         description: "Failed to fetch chat",
  //         variant: "destructive",
  //       });
  //     }
  //     setChat(json);
  //   })()
  //
  // }, [])

  useEffect(() => {
    msgFetchCounterRef.current = msgFetchCounter;
  }, [msgFetchCounter]);


  useEffect(() => {
    let isMounted = true;

    if (msgFetchCounter <= 0) {
      return;
    }

    (async () => {
      const { json, error } = await fetch_message();

      if (error) {
        toast({
          description: "Failed to fetch messages",
          variant: "destructive",
        })
        return;
      }

      if (!isMounted) {
        return console.warn("fetch message hook unmounted");
      }

      setMsgFetchCounter(prev => prev - 1);
      setMessages(prev => {
        const ids = new Set(prev.map(item => item.id));
        const items = json.items?.filter(item => !(ids.has(item.id))) || []
        return [...items.reverse(), ...prev]
      })

      if (json.next_url) {
        const url = new URL(json.next_url);
        setNextMsgURL(`${baseMsgURL}${url.search}`);
      } else {
        setNextMsgURL(null);
        setMsgFetchCounter(0);
      }
    })()

    return () => {
      isMounted = false
    }

  }, [msgFetchCounter])


  useEffect(() => {

    const handleEventListener = () => {
      const node = messagesListRef.current;

      if (node.scrollTop > 400 || msgFetchCounterRef.current > 0 || !nextMsgURL) {
        return;
      }

      console.log("searching for previous chats")
      setMsgFetchCounter(3);

    }

    messagesListRef.current?.addEventListener("scroll", handleEventListener);


    return () => {
      messagesListRef.current?.removeEventListener("scroll", handleEventListener);
    }

  }, []);

  const handleSendMessage = (e) => {
    e.preventDefault();

    if (!input) return;

    setMessages((messages) => [
      ...messages,
      {
        id: messages.length + 1,
        message: input,
        variant: "sent",
      },
    ]);

    setInput("");
    formRef.current?.reset();
  }

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      handleSendMessage(e);
    }
  };

  const fetch_message = async () => {
    return await auth_request(
      nextMsgURL,
      {
        method: "GET",
      }
    )
  }

  const handle_message = async (unmounted = false) => {

    if (!nextMsgURL) {
      setMsgFetchCounter(0);
      return;
    }

    const { json, error } = await auth_request(
      nextMsgURL,
      {
        method: "GET",
      }
    )

    if (error) {
      toast({
        description: "Failed to fetch messages",
        variant: "destructive",
      })
      return;
    }

    if (unmounted) {
      return console.warn("component was unmounted")
    }

    setMessages(prev => {
      const ids = new Set(prev.map(item => item.id));
      const items = json.items.filter(item => !(ids.has(item.id)))
      return [...items.reverse(), ...prev]
    })

    if (json.next_url) {
      const url = new URL(json.next_url);
      setNextMsgURL(`${baseMsgURL}${url.search}`);
    } else {
      setNextMsgURL(null);
      // setMsgFetchCounter(0);
    }
  }


  return (
    <div className="text-white border border-red-500 flex w-full flex-col h-[600px]" ref={ref}>
      <div className="flex-1 w-full overflow-y-auto bg-muted/40">
        <ChatMessageList ref={messagesListRef}>
          <AnimatePresence>
            {
              user && messages.map((message, index) => {

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
                    <ChatBubble key={index} variant={message.sender === user.id ? "sent" : "received"}>
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
            onKeyDown={handleKeyDown}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message here..."
            className="min-h-12 resize-none rounded-lg bg-background border-0 p-3 shadow-none focus-visible:ring-0"
          ></ChatInput>
          <div className="flex items-center p-3 pt-0">
            <Button variant="ghost" size="icon">
              <Paperclip className="size-4" />
              <span className="sr-only">Attach file</span>
            </Button>

            <Button variant="ghost" size="icon">
              <Mic className="size-4" />
              <span className="sr-only">Use Microphone</span>
            </Button>

            <Button
              // disabled={!input || isLoading}
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

  )
}

export default forwardRef(ChatBox);
