import useAuth from "@/hooks/useAuth";
import { Button } from "@/components/ui/button"

const Index = () => {

  const { logout } = useAuth();
  return (
    <div>
      {/* <Button onClick={logout}> */}
      {/*   Logout */}
      {/* </Button> */}
    </div>

  )
}
export default Index
