
import useAuth from "@/hooks/useAuth"
import { Navigate, Outlet } from "react-router";

const UnProtectedLayout= () => {
  const {logged} = useAuth();

  if (logged === true){
    return <Navigate to="/" replace />
  } else if (logged === null){
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

  return <Outlet/>
}
export default UnProtectedLayout
