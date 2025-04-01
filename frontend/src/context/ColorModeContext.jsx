import { createContext, useState } from "react"

const ColorModeContext = createContext({
    mode: "system",
    toggleMode: () => {}
})

const ColorModeContextProvider = ({children}) => {
    const [mode, setMode] = useState(import.meta.env.VITE_DEFAULT_COLOR_MODE ?? "dark")

    const toggleMode = () => {
        setMode(prev => prev == "dark" ? "light": "dark")
    }

    return (
        <ColorModeContext.Provider value={{
            mode,
            toggleMode
        }}>
            {children}
        </ColorModeContext.Provider>
    )
}



export {
    ColorModeContext,
    ColorModeContextProvider
}
