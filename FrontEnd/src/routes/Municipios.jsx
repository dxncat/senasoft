import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

function Municipios() {
    const [dataMunicipios, setDataMunicipios] = useState('')

    useEffect(() => {
        const municipios = fetch('http://localhost:8000/municipios/')
        municipios
            .then((info) => info.json())
            .then(lectura => {
                setDataMunicipios(lectura.map(
                    dato =>
                        <tr key={dato.id}>
                            <td>{dato.nombre}</td>
                            <td>{<Link to={'/municipios/update/' + dato.id} className='link_actualizar'> Actualizar</Link>}</td>
                            <td>{<Link to={'/municipios/update/' + dato.id} className='link_eliminar'> Eliminar</Link>}</td>
                        </tr>
                ))
            })
            .catch(() => console.log('se ha producido un error'))
    }, [])

    return (
        <>
            <h1>
                Municipios Registrados
            </h1>
            <table className='table table-hover'>
                <thead>
                    <tr>
                        <th>Nombre</th>
                        <th>Actualizar</th>
                        <th>Eliminar</th>
                    </tr>
                </thead>
                <tbody>
                    {dataMunicipios}
                </tbody>
            </table>
        </>
    )
}

export default Municipios