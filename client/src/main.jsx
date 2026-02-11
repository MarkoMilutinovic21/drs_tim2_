import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)

// iz index.html uzme jedan prazan div - to je mesto gde ce sve napraviti i renderovati kao jednu komponentu
// strinct mode je da salje upozorenja u konzolu