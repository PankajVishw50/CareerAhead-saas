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

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <SettingsContextProvider>
      <ColorModeContextProvider>
        <LocalDBContextProvider>
          <AuthContextProvider>
            <WalletContextProvider>
              <ChatContextProvider>
                <App />
              </ChatContextProvider>
              <Toaster />
            </WalletContextProvider>
          </AuthContextProvider>
        </LocalDBContextProvider>
      </ColorModeContextProvider>
    </SettingsContextProvider>
  </StrictMode>
)
