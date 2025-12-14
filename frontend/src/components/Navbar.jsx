import React from "react";
import { Link } from "react-router-dom";
import "./Navbar.css";
import logo from '../plantLogo.png'

export default function Navbar() {
  return (
    <nav className="navbar">
      <div className="left">
        <img src={logo} alt="logo" />
        <h2 className="logo">Almighty</h2>
      </div>
      <ul className="nav-links">
          <li><Link to="/">Home</Link></li>
          <li><Link to="/how-it-works">Anything</Link></li>
          <li><Link to="/about">About</Link></li>
          <li><Link to="/contact">Contact</Link></li>
      </ul>
      <div className="try-btn">
        <button>Try for free</button>
      </div>
    </nav>

  );
}
