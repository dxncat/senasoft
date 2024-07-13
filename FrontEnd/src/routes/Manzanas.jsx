import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

function Manzanas() {
    const [dataManzanas, setDataManzanas] = useState('')

    useEffect(() => {
        const manzanas = fetch('http://localhost:8000/manzanas/')
        manzanas
            .then((info) => info.json())
            .then(lectura => {
                setDataManzanas(lectura.map(
                    dato =>
                        <tr key={dato.id}>
                            <td>{dato.nombre}</td>
                            <td>{dato.localidad}</td>
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
                Manzanas Registradas
            </h1>
            <table className='table table-hover'>
                <thead>
                    <tr>
                        <th>Nombre</th>
                        <th>Localidad</th>
                        <th>Dirección</th>
                        <th>Actualizar</th>
                        <th>Eliminar</th>
                    </tr>
                </thead>
                <tbody>
                    {dataManzanas}
                </tbody>
            </table>
        </>
    )
}

export default Manzanas