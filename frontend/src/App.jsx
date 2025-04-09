import { useState } from 'react'
import { Button } from './components/ui/button'
import useColorMode from './hooks/useColorMode'
import ProtectedLayout from './layouts/ProtectedLayout'
import Login from './pages/Login'
import { BrowserRouter, Routes, Route } from "react-router"
import DashboardLayout from './layouts/DashboardLayout'
import Index from './pages/Index'
import MarketPage from './pages/MarketPage'
import UnProtectedLayout from "@/layouts/UnProtectedLayout";

function App() {
  const {mode} = useColorMode()

  return (
    <BrowserRouter>
    <div className={
      "main " + mode
    }>
        <Routes utes>
          <Route element={<UnProtectedLayout/>} >
            <Route path="/login" element={<Login/>} />
          </Route>

          <Route element={<ProtectedLayout/>}>
            <Route element={<DashboardLayout/>}>
              <Route path="/" element={<Index/>} />
              <Route path="/market" element={<MarketPage/>} />
            </Route>
          </Route>

        </Routes>
    </div>

    </BrowserRouter>
  )
}

export default App
