import { urls } from "@/utils/urls";
import { createContext } from "react";

const SettingsContext = createContext({
  api_url: null,
  api_base_url: null,
  urls: {},
});

const SettingsContextProvider = ({children}) => {


  return <SettingsContext.Provider value={{
    api_url: import.meta.env.VITE_API_URL,
    api_base_url: import.meta.env.VITE_API_BASE_URL,
    urls: urls,
  }}> {children} </SettingsContext.Provider>
}

export {
  SettingsContext,
  SettingsContextProvider,
}
