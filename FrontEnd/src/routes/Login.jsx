import React, { useState, useContext } from 'react'
import { useNavigate } from 'react-router-dom';
import { TokenContext } from '../context/TokenContext'
import MensajeError from '../components/MensajeError'
import { Link } from 'react-router-dom'

function Login() {

    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [mensajeError, setMensajeError] = useState('')
    const [, setToken] = useContext(TokenContext)
    const navigate = useNavigate();

    const submitInicioS = async () => {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
        };

        try {
            const response = await fetch('http://localhost:8000/mujeres/acceso', requestOptions);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Error al iniciar sesión');
            }

            setToken(data.access_token);
            navigate('/');
        } catch (error) {
            setMensajeError(error.message);
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        submitInicioS();
    };

    return (
        <>
            <form action="" onSubmit={handleSubmit}>
                <label>Documento</label>
                <input
                    required
                    type="number"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder='Ingresa aquí tu numero de documento'
                />
                <label>Contraseña</label>
                <input
                    required
                    type="password"
                    value={password}
                    placeholder='Ingresa aquí tu contraseña'
                    onChange={(e) => setPassword(e.target.value)}
                />
                <MensajeError mensaje={mensajeError} />
                <span>No tienes una cuenta? <Link to={'/registro'}>Regístrate</Link></span>
                <input type="submit" value="Iniciar Sesión" />
            </form>
        </>
    )
}

export default Login