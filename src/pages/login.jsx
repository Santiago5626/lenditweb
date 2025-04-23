import React from 'react';
import { useNavigate } from 'react-router-dom';
import logo from '../images/logo.png';

const Login = () => {
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    // Here you can add authentication logic if needed
    navigate('/inicio');
  };

  return (
    <div className="container min-vh-100 d-flex justify-content-center align-items-center bg-light p-4 font-sans">
      <div className="d-flex rounded shadow overflow-hidden w-100" style={{ maxWidth: '900px', transition: 'transform 0.3s', backgroundColor: '#00304D' }}>
        <div className="flex-fill d-flex justify-content-center align-items-center p-4 position-relative overflow-hidden" style={{ backgroundColor: '#00304D' }}>
          <div className="position-absolute top-0 start-0 w-100 h-100 opacity-25" style={{ background: 'radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 70%)', zIndex: 0 }}></div>
          <img
            src={logo}
            alt="Logo"
            className="img-fluid" 
            style={{ maxWidth: '250px', zIndex: 1, filter: 'drop-shadow(0 0 0.75rem rgba(0,0,0,0.3))' }}
          />
        </div>
        <div className="flex-fill bg-white p-4 d-flex flex-column justify-content-center">
          <h1 className="text-primary fw-bold mb-4 text-center position-relative pb-2" style={{ borderBottom: '3px solid #00304D', width: 'fit-content', margin: '0 auto' }}>
            Bienvenido
          </h1>
          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <input
                type="text"
                id="usuario"
                name="usuario"
                placeholder="Usuario"
                required
                className="form-control"
              />
            </div>
            <div className="mb-3">
              <input
                type="password"
                id="contrasena"
                name="contrasena"
                placeholder="Contraseña"
                required
                className="form-control"
              />
            </div>
            <div className="text-end mb-3">
              <a
                href="/forgot-password"
                className="text-muted text-decoration-underline"
                style={{ cursor: 'pointer' }}
              >
                ¿Has olvidado tu contraseña?
              </a>
            </div>
            <button
              type="submit"
              className="btn btn-primary w-100 fw-semibold shadow-sm"
              style={{ transition: 'all 0.3s' }}
              onMouseDown={e => e.currentTarget.style.transform = 'translateY(2px)'}
              onMouseUp={e => e.currentTarget.style.transform = 'translateY(0)'}
              onMouseLeave={e => e.currentTarget.style.transform = 'translateY(0)'}
            >
              Iniciar sesión
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Login;
