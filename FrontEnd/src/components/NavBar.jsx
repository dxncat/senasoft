import React, {useContext} from 'react'
import { TokenContext } from '../context/TokenContext'
import { NavLink } from 'react-router-dom'

function NavBar() {
    const [token, setToken] = useContext(TokenContext)


    const logout = () => {
        setToken(null)
        localStorage.removeItem('token')
    }

    const navLinks = [{ name: 'Inicio', path: '/' }, { name: 'Municipios', path: '/municipios' }, { name: 'Manzanas', path: '/manzanas' }, { name: 'Establecimientos', path: '/establecimientos' }, { name: 'Agendas', path: '/agendas' }].map((link, index) => (
        <NavLink key={index} to={link.path}> {link.name}</NavLink>
    ))

    return (
        <nav className='barra_navegacion'>
            <section className='logo'>
                <img src="/logo.png" alt="SENA" className='logo' />
                <NavLink to={'/'}><h1>SenaSoft</h1></NavLink>
            </section>
            <section>
                {!token && <NavLink to={'/login'}>Inicia Sesión/Regístrate</NavLink>}
                {navLinks}
                {token && <button onClick={logout}>Cerrar Sesión</button>}
            </section>
        </nav>
    )
}

export default NavBar