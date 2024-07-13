import React from 'react'

function MensajeError({ mensaje }) {
  return (
    <p className="error_message">
        {mensaje}
    </p>
  )
}

export default MensajeError