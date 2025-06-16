import React from 'react';

const PageHeader = ({ title, actionButton }) => {
    return (
        <div className="circulacion-header">
            <h1>{title}</h1>
            {actionButton}
        </div>
    );
};

export default PageHeader;
