import React from 'react';

const AlertMessage = ({ type = 'danger', message }) => {
    if (!message) return null;

    return (
        <div className={`alert alert-${type}`} role="alert">
            {message}
        </div>
    );
};

export default AlertMessage;
