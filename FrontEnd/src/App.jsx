import { useState, useEffect, useContext } from "react"
import NavBar from "./components/NavBar"
import Login from "./routes/Login"
import Municipios from "./routes/Municipios"
import Manzanas from "./routes/Manzanas"
import Establecimientos from "./routes/Establecimientos"
import Error404 from "./routes/Error404"
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import './App.css'
import { TokenContext } from "./context/TokenContext"
import Home from "./routes/Home"

function App() {
  const [nombres, setNombres] = useState('')
  const [apellidos, setApellidos] = useState('')
  const [token, setToken] = useContext(TokenContext)

  const getUser = async () => {
    const requestOptions = {
      method: 'GET',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` }
    }
    const response = await fetch('http://localhost:8000/mujeres/me', requestOptions)
    const data = await response.json()
    if (!response.ok) {
      console.log('Error al obtener el usuario')
    } else {
      setNombres(data.nombre)
      setApellidos(data.apellido)
    }
  }

  useEffect(() => {
    if (token) {
      getUser()
    } else {
      setNombres('')
      setApellidos('')
    }
  }, [token])

  return (
    <BrowserRouter>
      <NavBar />
      <Routes>
        <Route path='/' element={<Home nombres={nombres} apellidos={apellidos} />} />
        <Route path='/login' element={<Login />} />
        <Route path='/municipios' element={<Municipios />} />
        <Route path='/manzanas' element={<Manzanas />} />
        <Route path='/establecimientos' element={<Establecimientos />} />
        <Route path='/*' element={<Error404 />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
