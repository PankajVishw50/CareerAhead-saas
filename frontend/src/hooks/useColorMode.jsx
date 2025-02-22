import { ColorModeContext } from "@/context/ColorModeContext"
import { useContext } from "react"

const useColorMode = () => {
  const context = useContext(ColorModeContext);

  return context
}
export default useColorMode