import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { useState } from "react"



const SessionsWindow = () => {

  const [sessions, setSessions] = useState();

  return (
    <Card
      className="w-full max-w-md"
    >

      <CardContent>



      </CardContent>
      <CardFooter>
        <span className="flex w-full justify-center">
          See All sessions
        </span>
      </CardFooter>

    </Card>
  )
}

export default SessionsWindow
