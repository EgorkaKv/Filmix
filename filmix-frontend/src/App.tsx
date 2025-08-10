//import { React } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import HomePage from './pages/HomePage'
import AddMoviePage from './pages/AddMoviePage'
import './App.css'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/add-movie" element={<AddMoviePage />} />
      </Routes>
    </Router>
  )
}

export default App
