import { LoginForm } from "@/components/login-form"
import { GalleryVerticalEnd } from "lucide-react"
import {Navigate} from "react-router";

import useAuth from "@/hooks/useAuth";


const Login = () => {
  return (
    <div className="flex min-h-svh h-screen flex-col items-center justify-center gap-6 bg-muted p-6 md:p-10">
      <div className="flex w-full max-w-sm flex-col gap-6">
        <a href="#" className="flex items-center gap-2 self-center font-medium text-white">
          <div className="flex h-6 w-6 items-center justify-center rounded-md bg-primary text-primary-foreground">
            <GalleryVerticalEnd className="size-4" />
          </div>
          CareerAhead
        </a>
        <LoginForm />
      </div>
    </div>
  )
}
export default Login
