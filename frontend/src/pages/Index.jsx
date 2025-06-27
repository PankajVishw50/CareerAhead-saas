import useAuth from "@/hooks/useAuth";
import { Button } from "@/components/ui/button"
import SessionsWindow from "@/components/SessionsWindow";

const Index = () => {

  const { logout } = useAuth();
  return (
    <div>
      <SessionsWindow />
    </div>

  )
}
export default Index
