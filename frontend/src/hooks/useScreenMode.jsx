import { ScreenModeContext } from "@/context/ScreenModeContext"
import { useContext } from "react"

const useScreenMode = () => {
  return useContext(ScreenModeContext)
}

export default useScreenMode
