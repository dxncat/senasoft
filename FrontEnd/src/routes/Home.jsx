import React from 'react'

function Home({ nombres, apellidos }) {
    console.log(nombres)
    console.log(apellidos)
    return (
        <>
            <h1>Home</h1>
            <p>Bienvenida a la página principal {nombres} {apellidos}!</p>
        </>
    )
}

export default Home