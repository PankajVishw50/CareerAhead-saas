import { WebSocketContext } from "@/context/WebSocketContext"
import { useContext } from "react"

const useWebSocket = () => {
  return useContext(WebSocketContext)
}

export default useWebSocket
