import ChatBox from "@/components/ChatBox";

const ChatPage = ({ chat_id = null }) => {
  return (
    <ChatBox chat_id={chat_id} />
  )
}

export default ChatPage;
