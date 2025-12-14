import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Footer from "./components/Footer";
import About from "./pages/About";
import HowItWorks from "./pages/HowItWorks";
import Contact from "./pages/Contact";
import TryForFree from "./pages/TryForFree";

function App() {
  return (
    <Router>
      {/* <h3 className="message">Let's take care of <s>ur</s> our plants.</h3> */}
      <Navbar />
      <div className="container">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/how-it-works" element={<HowItWorks />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/try-for-free" element={<TryForFree />} />
        </Routes>
      </div>
      <Footer />
    </Router>
  );
}

export default App;
