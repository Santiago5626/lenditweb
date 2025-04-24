import React from 'react';
import './TablaUsuarios.css';
const usuarios = [
  ['Samantha Harris', '1004368358', '3002221112', 'sharris@yahoo.com', '2877062', 'ADSO'],
  ['Sarah Allen', '1065852147', '3002221113', 'sallen@yahoo.com', '2877062', 'ADSO'],
  ['Andrew Walker', '4268512', '3002221117', 'awalker@yahoo.com', '2877062', 'ADSO'],
  ['Andrew Taylor', '1007254125', '3002221114', 'taylorandrew@hotmail.com', '2877062', 'ADSO'],
  ['Sarah White', '1004325585', '3002221118', 'swhite@gmail.com', '2877062', 'ADSO'],
  ['John Hill', '1002254152', '3002221115', 'johnhill@yahoo.com', '2877062', 'ESPECIES M.'],
  ['Ashley Gonzalez', '1066525896', '3215426294', 'agonzalez@yahoo.com', '2877062', 'ESPECIES M.'],
  ['Nathan Wood', '1065852141', '3154562620', 'nathanwood91@gmail.com', '2877062', 'GANADERIA'],
];

const TablaUsuarios = () => {
  return (
    <div className="container my-4">
      <div className="d-flex gap-2 mb-3">
        <input type="text" className="form-control" placeholder="Número de ID" />
        <input type="text" className="form-control" placeholder="Ficha" />
        <button className="btn btn-outline-danger"><span className="material-symbols-outlined">delete</span></button>
        <button className="btn btn-outline-primary"><span className="material-symbols-outlined">person_edit</span></button>
        <button className="btn btn-outline-success"><span className="material-symbols-outlined">person_add</span></button>
      </div>

      <table className="table table-bordered table-hover">
        <thead className="thead-light">
          <tr>
            <th>Check</th>
            <th>Nombre</th>
            <th>Número de ID</th>
            <th>Teléfono</th>
            <th>Correo</th>
            <th>Ficha</th>
            <th>Programa</th>
          </tr>
        </thead>
        <tbody>
          {usuarios.map((user, index) => (
            <tr key={index}>
              <td><input type="checkbox" /></td>
              {user.map((data, i) => <td key={i}>{data}</td>)}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TablaUsuarios;
