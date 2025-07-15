import { toast } from "@/hooks/use-toast";
import useAuth from "@/hooks/useAuth";
import { get_param_url } from "@/utils/collections";
import { urls } from "@/utils/urls";
import { createContext, useEffect, useState } from "react"

const WebSocketContext = createContext({
  ws: null,
});

const WebSocketContextProvider = ({ children }) => {
  const { logged, auth_request } = useAuth();

  const [signedToken, setSignedToken] = useState(null);
  const [ws, setWs] = useState(null);
  const ws_notification_url = get_param_url(urls.ws_notification.get_url(), { token: signedToken });
  const [subscribers, setSubscribers] = useState({});
  const [queues, setQueues] = useState({});

  // Fetch Signed Token
  useEffect(() => {
    // Ignore if not logged
    // or already fetched
    if (!logged || signedToken) {
      return;
    }

    // Fetch Signed Token
    fetch_signed_token();

  }, [logged]);

  // Create connection
  useEffect(() => {

    if (!signedToken) {
      return
    }

    const _ws = new WebSocket(ws_notification_url)

    _ws.onopen = (e) => {
      console.log("WS Connection opened:", e);
    }

    _ws.onclose = (e) => {
      console.log("WS Connection closed:", e);
    }

    _ws.onerror = (e) => {
      console.log("WS Connection error:", e);
    }

    _ws.onmessage = (e) => {
      let json = null
      try {
        json = JSON.parse(e.data);
      } catch (error) {
        console.warn("Failed to JSON parse the WS data: ", e.data);
      }
      handle_message(json || e.data)
    }

    setWs(_ws);

    return (() => {
      _ws.close();
      console.log("WS Connection closed by unmounting")
    });

  }, [signedToken]);

  useEffect(() => {
    for (let [k, v] of Object.entries(queues)) {
      let index = 0;

      // Send Message to each subscriber
      for (let subscriber of (subscribers[k] || [])) {
        if ((subscriber.pointer + 1) < v.length) {
          subscriber.setQueue(prev => {
            return [...prev, ...v.slice(subscriber.pointer + 1)]
          });

          // Update subscriber's pointer
          setSubscribers(prev => {
            const _d = [...prev[k]]
            const _index = _d.findIndex(element => element.id === subscriber.id)
            if (_index !== -1) {
              _d[_index] = { ..._d[_index], pointer: v.length - 1 }
            }
            return {
              ...prev,
              [k]: _d
            }
          });
        }
        index++;
      }
    }
  }, [queues, subscribers]);

  const _fetch_signed_token = async () => {
    return await auth_request(
      urls.signed_token.get_url(),
      {
        method: "GET",
      }
    );
  }

  const fetch_signed_token = async () => {
    const { json, error } = await _fetch_signed_token()
    if (error) {
      return toast({
        description: "Failed to fetch signed token",
        variant: "destructive",
      })
    }
    setSignedToken(json.token)
  }

  const subscribe = (message_type, id, setQueue) => {
    setSubscribers(prev => {
      return {
        ...prev,
        [message_type]: [...(prev[message_type] || []), { id, message_type, setQueue, pointer: -1 }]
      }
    });
  }

  const unsubscribe = (message_type, id) => {
    setSubscribers(prev => {
      const index = prev[message_type]?.findIndex(subscriber => subscriber.id == id);
      if (index === -1) {
        return prev;
      }

      const _q = [...(prev[message_type] || [])];
      _q.splice(index, 1);
      return {
        ...prev,
        [message_type]: _q,
      }
    })
  }

  const send = (data) => {
    if (!ws || ws.OPEN !== 1) {
      return false;
    }

    ws.send(data);
    return true
  }

  const handle_message = (message) => {

    setQueues(prev => {
      return {
        ...prev,
        [message.type || ""]: [...(prev[message.type] || []), message]
      }
    });

  }

  return <WebSocketContext.Provider
    value={{
      ws,
      subscribe,
      unsubscribe,
      send,
    }}
  >
    {children}
  </WebSocketContext.Provider>

}

export {
  WebSocketContext,
  WebSocketContextProvider,
}
