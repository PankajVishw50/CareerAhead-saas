import { toast } from "@/hooks/use-toast";
import useAuth from "@/hooks/useAuth";
import useWebSocket from "@/hooks/useWebSocket";
import { get_param_url } from "@/utils/collections";
import { urls } from "@/utils/urls";
import { constructNow } from "date-fns";
import { createContext, useEffect, useState } from "react";

const ChatContext = createContext();

const SUBSCRIBER_NEW_MESSAGE_QUEUE_ID = "chatContext.messages.new";
const SUBSCRIBER_SEEN_MESSAGE_QUEUE_ID = "chatContext.messages.seen";

const ChatContextProvider = ({ children }) => {
  const { auth_request, user } = useAuth();
  const { subscribe, unsubscribe, send } = useWebSocket();

  const [chats, setChats] = useState([]);
  const [fetchChatUrl, setFetchChatUrl] = useState(get_param_url(urls.chats.get_url(), { type: "all", size: 20 }));
  const [messages, setMessages] = useState({});
  const [chatsMeta, setChatsMeta] = useState({});
  const [messageQueue, setMessageQueue] = useState([]);
  const [messageSeenQueue, setMessageSeenQueue] = useState([]);

  // To fetch chats
  useEffect(() => {
    if (!fetchChatUrl) {
      return;
    }
    fetch_chats();
  }, [fetchChatUrl])

  // To rearrange chats
  useEffect(() => {
    add_chats(chats, []);
  }, [messages])


  // To Fetch Messages
  useEffect(() => {

    for (let chatM of Object.values(chatsMeta)) {
      if (chatM.fetch_counter <= 0 || chatM.failed_consecutive > 5 || chatM.fetching) {
        continue;
      }
      _fetch_messages(chatM.id);
    }

  }, [chatsMeta]);

  // Subscribe queue to websocket to receive new messages and seen
  useEffect(() => {
    subscribe("message.new", SUBSCRIBER_NEW_MESSAGE_QUEUE_ID, setMessageQueue);
    subscribe("message.seen", SUBSCRIBER_SEEN_MESSAGE_QUEUE_ID, setMessageSeenQueue);

    return () => {
      unsubscribe("message.new", SUBSCRIBER_NEW_MESSAGE_QUEUE_ID);
      unsubscribe("message.seen", SUBSCRIBER_SEEN_MESSAGE_QUEUE_ID,)
    }
  }, []);

  // Update messages queues when new web socket message is received
  useEffect(() => {

    if (messageQueue.length <= 0) {
      return;
    }

    const messages_collection = {}

    for (let messageE of messageQueue) {
      const message = messageE.text.payload;
      if (!messages_collection[message.chat]) {
        messages_collection[message.chat] = [];
      }
      messages_collection[message.chat].push(message);
    }

    for (let [key, messages] of Object.entries(messages_collection)) {
      add_messages(key, messages, false);
    }
    setMessageQueue([]);

  }, [messageQueue])

  useEffect(() => {
    if (messageSeenQueue.length <= 0) {
      return;
    }

    for (let _notification of messageSeenQueue) {
      const notification = _notification.payload;
      update_seen(notification.chat_id, false, notification.id);
    }
    setMessageSeenQueue([]);

  }, [messageSeenQueue])

  // Chat
  const get_chat = (chat_id) => {
    const chat = chats.find(item => item.id === chat_id);
    return chat
  }

  const _add_chat = (chats, nchat) => {
    const cchats = chats.slice()
    const ncm = recent_message(nchat.id)
    const num = count_unseen_messages(nchat.id);
    const now = constructNow();

    const ncchat = cchats.find(item => item.id === nchat.id)
    if (ncchat) {
      cchats.splice(cchats.indexOf(ncchat), 1);
    }

    // 1. Chats with unseen messages
    // 2. Active chats
    // 3. upcoming chats
    // 4. most recent message

    let i = 0;
    while (i <= cchats.length) {
      const ichat = cchats[i];
      const icm = recent_message(ichat?.id)
      const ium = count_unseen_messages((ichat?.id));

      if (i >= cchats.length) {
        // Insert if no chat is remained
        cchats.splice(i, 0, nchat);
        break;
      } else if (num || ium) {
        // One of chat have unseen message
        if (
          num && (
            !ium || (
              ncm.created_at_at >= icm.created_at_dt
            )
          )
        ) {
          cchats.splice(i, 0, nchat);
          break;
        }
      } else if (nchat.is_active || ichat.is_active) {
        // Active Chats
        if (
          nchat.is_active && (
            !ichat.is_active || (
              ncm && (
                !icm || ncm.created_at_dt >= icm.created_at_dt
              )
            )
          )
        ) {
          cchats.splice(i, 0, nchat);
          break;
        }
      } else if (nchat.session_from_datetime_dt > now || ichat.session_from_datetime_dt > now) {
        // Upcoming Chats
        if (
          nchat.session_from_datetime_dt > now && (
            ichat.session_from_datetime_dt < now || (
              ncm && (
                !icm || ncm.created_at_dt >= icm.created_at_dt
              )
            )
          )
        ) {
          cchats.splice(i, 0, nchat);
          break;
        }
      } else if (ncm || icm) {
        if (
          ncm && (
            !icm || ncm.created_at_dt >= icm.created_at_dt
          )
        ) {
          cchats.splice(i, 0, nchat);
          break;
        }
      } else {
        if (nchat.created_at_dt >= ichat.created_at_dt) {
          cchats.splice(i, 0, nchat);
          break;
        }
      }
      i++;
    }

    return cchats
  }

  const add_chat = (chat, cchats = chats) => {
    const pchat = {
      ...chat,
      created_at_dt: new Date(chat.created_at),
      session_from_datetime_dt: new Date(chat.session_from_datetime),
    }
    const nchats = _add_chat(cchats, pchat);
    if (messages[pchat.id] === undefined) {
      messages[pchat.id] = []
    }


    // Don't update chat meta if already parsent
    if (chatsMeta[pchat.id] === undefined) {
      setChatsMeta(prev => {
        return {
          ...prev,
          [pchat.id]: {
            ...prev[pchat.id],
            id: pchat.id,
            nextFetchUrl: urls.messages.get_url(pchat.id),
            fetch_counter: 2,
            failed_consecutive: 0,
            fetching: prev[pchat.id]?.fetching ?? false
          }
        }
      });
    }

    setChats(nchats);
    return nchats;
  }

  const add_chats = (nchats, cchats = chats) => {
    let pchats = cchats.slice();

    for (let nchat of nchats) {
      pchats = add_chat(nchat, pchats);
    }

    return cchats
  }

  const fetch_chat = async (chat_id, refetch = false) => {

    if (
      get_chat(chat_id) && !refetch
    ) {
      return true;
    }

    const { json, error } = await auth_request(
      urls.chat.get_url(chat_id),
      {
        method: "GET"
      }
    );

    if (error) {
      toast({
        description: "Failed to fetch messages",
        variant: "destructive",
      });
      return false;
    }

    add_chat(json);
    return true;
  }

  const fetch_chats = async () => {

    const { json, error } = await auth_request(
      fetchChatUrl,
      {
        method: "GET"
      }
    );

    if (error) {
      return toast({
        description: "failed to fetch chats",
        variant: "destructive"
      });
    }

    add_chats(json.items)
    setFetchChatUrl(json.next_url);
  }

  const get_ordered_chat = () => {
    let o_chats = [];
    for (let chat of chats) {
      o_chats = _add_chat(o_chats, chat);
    }
    return o_chats
  }

  // Messages
  const get_messages = (chat_id) => {
    return messages[chat_id] !== undefined ? messages[chat_id] : []
  }

  const recent_message = (chat_id, u = null) => {
    let ms = get_messages(chat_id)
    if (u === true) {
      ms = get_messages(chat_id).filter(message => message.sender === user.id);
    } else if (u === false) {
      ms = get_messages(chat_id).filter(message => message.sender === get_chat_user(chat_id));
    }
    return ms?.[0]
  }

  const count_unseen_messages = (chat_id) => {
    if (!user) {
      return 0
    }
    const messages = get_messages(chat_id)
    const unseen_messages = messages.filter(message => !message.seen && message.sender != user.id);
    return unseen_messages.length;
  }

  // Users are already present in chat data, hence this function is redency
  const _get_chat_users = (chat_id) => {
    const users = [null, null];
    const messages = get_messages(chat_id)
    messages.forEach(message => {
      if (users[0] === null) {
        users[0] = message.sender;
      } else if (users[1] === null && message.sender != users[0]) {
        users[1] = message.sender;
      }
    });
    return users
  }

  const get_chat_user = (chat_id) => {
    const chat = get_chat(chat_id)
    return chat.user_a === user.id ? chat.user_b : chat.user_a
  }

  const update_seen = (chat_id, u = true, message_id = null) => {
    if (!get_chat(chat_id)) {
      return false;
    }

    const messages = [...get_messages(chat_id)];
    const sender = u ? get_chat_user(chat_id) : user.id;
    const message_index = message_id === null ? 0 : messages.findIndex(message => message.id === message_id);
    if (message_index === -1) {
      return false;
    }
    for (let i = message_index; i < messages.length; i++) {
      if (messages[i].sender === sender) {
        messages[i].seen = true
      }
    }
    setMessages(prev => {
      return {
        ...prev,
        [chat_id]: messages,
      }
    });


    // Send ws message is user is true
    if (u) {
      send(JSON.stringify({
        type: "message.seen",
        payload: {
          chat_id: chat_id,
          id: messages[message_index].id,
        }
      }));
    }
  }

  const fetch_messages = (chat_id) => {
    setChatsMeta(prev => {
      return {
        ...prev,
        [chat_id]: {
          ...prev[chat_id],
          fetch_counter: prev[chat_id].fetch_counter + 3,
        }
      }
    });
  }

  const _fetch_messages = async (chat_id) => {
    const chat = get_chat(chat_id);
    const chatM = chatsMeta[chat_id]

    setChatsMeta(prev => {
      return {
        ...prev,
        [chat_id]: {
          ...prev[chat_id],
          fetching: true,
          fetch_counter: prev[chat_id].fetch_counter - 1,
        }
      }
    });

    const { json, error } = await auth_request(
      chatM.nextFetchUrl,
      {
        method: "GET"
      }
    );

    if (error) {
      setChatsMeta(prev => {
        return {
          ...prev,
          [chat_id]: {
            ...prev[chat_id],
            failed_consecutive: prev[chat_id].failed_consecutive + 1,
            fetching: false,
            fetch_counter: prev[chat_id].fetch_counter + 1
          }
        }
      });
      toast({
        description: "Failed to fetch messages",
        variant: "destructive",
      })
      return;
    }

    add_messages(chat_id, json.items)
    setChatsMeta(prev => {
      return {
        ...prev,
        [chat_id]: {
          ...prev[chat_id],
          nextFetchUrl: json.next_url,
          fetch_counter: json.next_url ? prev[chat_id].fetch_counter : 0,
          failed_consecutive: 0,
          fetching: false,
        }
      }
    });

  }

  const add_messages = (chat_id, nmessages, start = true) => {
    const ids = new Set(get_messages(chat_id).map(chat => chat.id));

    const pnmessages = nmessages?.filter(item => !ids.has(item.id));
    const filtered_messages = pnmessages.map(pnmessage => {
      return {
        ...pnmessage,
        created_at_dt: new Date(pnmessage.created_at),
        modified_at_dt: new Date(pnmessage.modified_at)
      }
    })

    setMessages(prev => {
      return {
        ...prev,
        [chat_id]: start ? [...(prev[chat_id] || []), ...filtered_messages] : [...filtered_messages, ...prev[chat_id]]
      }
    });
  }



  return <ChatContext.Provider value={{
    chats,
    get_chat,
    fetch_chat,
    setChats,
    add_chat,
    add_chats,
    get_ordered_chat,

    chatsMeta,

    messages,
    get_messages,
    recent_message,
    count_unseen_messages,
    fetch_messages,
    update_seen,
  }}>
    {children}
  </ChatContext.Provider>
}

export {
  ChatContext,
  ChatContextProvider,
}
