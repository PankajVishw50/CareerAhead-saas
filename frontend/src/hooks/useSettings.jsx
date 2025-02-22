import { SettingsContext } from "@/context/SettingsContext"
import { useContext } from "react"

const useSettings = () => {
  const context = useContext(SettingsContext);
  return context;
}

export {
  useSettings,
}