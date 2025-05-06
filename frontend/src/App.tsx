import {
  Box,
  Heading
} from '@chakra-ui/react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ListPage from "./pages/ListPage";
import FormPage from "./pages/FormPage";
import './App.css'

function App() {

  return (
    <Router>
      <Box p={4} maxW="800px" mx="auto">
        <Heading mb={4}>Avaiable Forms</Heading>
        <Routes>
          <Route path="/" element={<ListPage />} />
          <Route path="/form/:formId" element={<FormPage />} />
        </Routes>
      </Box>
    </Router>
  )
}

export default App
