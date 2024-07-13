import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

function Establecimientos() {
    const [dataEstablecimientos, setDataEstablecimientos] = useState('')

    useEffect(() => {
        const manzanas = fetch('http://localhost:8000/establecimientos/')
        manzanas
            .then((info) => info.json())
            .then(lectura => {
                setDataEstablecimientos(lectura.map(
                    dato =>
                        <tr key={dato.id}>
                            <td>{dato.nombre}</td>
                            <td>{dato.responsable}</td>
                            <td>{dato.direccion}</td>
                            <td>{<Link to={'/manzanas/update/' + dato.id} className='link_actualizar'> Actualizar</Link>}</td>
                            <td>{<Link to={'/manzanas/update/' + dato.id} className='link_eliminar'> Eliminar</Link>}</td>
                        </tr>
                ))
            })
            .catch(() => console.log('se ha producido un error'))
    }, [])
    return (
        <>
            <h1>
                Establecimientos Registradas
            </h1>
            <table className='table table-hover'>
                <thead>
                    <tr>
                        <th>Nombre</th>
                        <th>Responsable</th>
                        <th>Dirección</th>
                        <th>Actualizar</th>
                        <th>Eliminar</th>
                    </tr>
                </thead>
                <tbody>
                    {dataEstablecimientos}
                </tbody>
            </table>
        </>
    )
}

export default Establecimientos