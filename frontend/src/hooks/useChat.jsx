import { ChatContext } from "@/context/ChatContext"
import { useContext } from "react"

const useChat = () => {
  return useContext(ChatContext);
}

export default useChat
