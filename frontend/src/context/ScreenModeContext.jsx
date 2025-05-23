import { useEffect, useState } from "react";
import { createContext } from "react";
import { SettingsContextProvider } from "./SettingsContext";

const ScreenModeContext = createContext({
  screen_mode: null,
});

const ScreenModeContextProvider = ({ children }) => {
  const [ScreenMode, setScreenMode] = useState();

  const [queries,] = useState({
    mobile: matchMedia("(max-size: 640px)"),
    sm: matchMedia("(min-size: 640px) and (max-size: 768px)"),
    md: matchMedia("(min-size: 768px) and (max-size: 1024px)"),
    lg: matchMedia("(min-size: 1024px) and (max-size: 1280px)"),
    xl: matchMedia("(min-size: 1280px) and (max-size: 1536px)"),
    two_xl: matchMedia("(min-size: 1536px)"),
  });

  const get_mode = () => {
    if (queries.mobile.matches) return 'mobile';
    if (queries.sm.matches) return 'sm';
    if (queries.md.matches) return 'md';
    if (queries.lg.matches) return 'lg';
    if (queries.xl.matches) return 'xl';
    if (queries.two_xl.matches) return '2xl';
    return 'unknown';
  }


  useEffect(() => {
    const update_mode = () => {
      setScreenMode(get_mode())
    }

    Object.entries(queries).forEach(element => {
      console.log(element)
      const [, query] = element;
      query.addEventListener("change", update_mode);
    });

    return () => {
      Object.entries(queries).forEach(element => {
        const [, query] = element;
        query.removeEventListener("change", update_mode);
      });
    }
  }, [])

  return <ScreenModeContext.Provider value={{ mode: ScreenMode }}>{children}</ScreenModeContext.Provider>
}

export {
  ScreenModeContext,
  ScreenModeContextProvider,
}
