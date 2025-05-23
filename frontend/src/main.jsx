import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { ColorModeContextProvider } from './context/ColorModeContext'
import { AuthContextProvider } from './context/AuthContext'
import { SettingsContextProvider } from './context/SettingsContext'
import { LocalDBContextProvider } from './context/LocalDBContext'
import { WalletContextProvider } from './context/WalletContext'
import { Toaster } from './components/ui/toaster'
import { ChatContextProvider } from './context/ChatContext'
import { ScreenModeContextProvider } from './context/ScreenModeContext'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <ScreenModeContextProvider>
      <SettingsContextProvider>
        <ColorModeContextProvider>
          <LocalDBContextProvider>
            <AuthContextProvider>
              <WalletContextProvider>
                <App />
                <Toaster />
              </WalletContextProvider>
            </AuthContextProvider>
          </LocalDBContextProvider>
        </ColorModeContextProvider>
      </SettingsContextProvider>
    </ScreenModeContextProvider>
  </StrictMode>
)
