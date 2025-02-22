import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { ColorModeContextProvider } from './context/ColorModeContext'
import { AuthContextProvider } from './context/AuthContext'
import { SettingsContextProvider } from './context/SettingsContext'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <SettingsContextProvider>
      <ColorModeContextProvider>
        <AuthContextProvider>
          <App />
        </AuthContextProvider>
      </ColorModeContextProvider>
    </SettingsContextProvider>
  </StrictMode>,
)
