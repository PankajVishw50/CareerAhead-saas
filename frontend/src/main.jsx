import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { ColorModeContextProvider } from './context/ColorModeContext'
import { AuthContextProvider } from './context/AuthContext'
import { SettingsContextProvider } from './context/SettingsContext'
import { LocalDBContextProvider } from './context/LocalDBContext'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <SettingsContextProvider>
      <ColorModeContextProvider>
        <LocalDBContextProvider>
          <AuthContextProvider>
            <App />
          </AuthContextProvider>
        </LocalDBContextProvider>
      </ColorModeContextProvider>
    </SettingsContextProvider>
  </StrictMode>
)
