import { useState } from 'react'
import { Button } from './components/ui/button'
import Dashboard from './layouts/Dashboard'

function App() {
  const [count, setCount] = useState(0)

  return (
    <Dashboard></Dashboard>
  )
}

export default App
