import { ChatContextProvider } from "@/context/ChatContext";
import { WebSocketContextProvider } from "@/context/WebSocketContext";
import useAuth from "@/hooks/useAuth"
import { Navigate, Outlet } from "react-router";

const ProtectedLayout = () => {
  const { user, logged } = useAuth();

  if (logged === false) {
    return <Navigate to="/login" replace />
  } else if (logged === null) {
    return (
      <div className="h-screen flex justify-center items-center">
        <div className="animate-bounce">
          Loading
          <span>.</span>
          <span>.</span>
          <span>.</span>
        </div>
      </div>
    )
  }

  return (
    <WebSocketContextProvider>
      <ChatContextProvider>
        <Outlet />
      </ChatContextProvider>
    </WebSocketContextProvider>
  )
}
export default ProtectedLayout
