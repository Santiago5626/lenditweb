import React from 'react';
import './TablaResumenEstado.css';

const TablaResumenEstado = () => {
  return (
    <div className="status-box p-3 bg-light rounded shadow-sm text-dark">
      <table className="table table-bordered table-striped">
        <thead className="thead-dark">
          <tr>
            <th>Estado</th>
            <th>M</th>
            <th>PM</th>
            <th>MR</th>
            <th>MSD</th>
            <th>G</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Disponibles</td>
            <td>15</td>
            <td>43</td>
            <td>76</td>
            <td>9</td>
            <td>45</td>
          </tr>
          <tr>
            <td>No disponibles</td>
            <td>43</td>
            <td>56</td>
            <td>82</td>
            <td>51</td>
            <td>90</td>
          </tr>
        </tbody>
      </table>
      <p className="footer-text text-muted small mt-2">
        [M] Mouse | [PM] Padmouse | [MR] Morral | [MSD] Micro SD |
      </p>
    </div>
  );
};

export default TablaResumenEstado;
