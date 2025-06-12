import React from "react";

const PaginationControls = ({
    currentPage = 1,
    totalPages = 1,
    totalItems = 0,
    itemsPerPage = 10,
    onPageChange = () => { },
    onItemsPerPageChange = () => { }
}) => {
    console.log('PaginationControls - Props:', {
        currentPage,
        totalPages,
        totalItems,
        itemsPerPage,
        shouldShow: totalItems > 0 && totalPages > 1
    });

    // Solo mostrar paginación si hay elementos Y más de una página
    if (totalItems === 0) {
        console.log('PaginationControls - No hay elementos, no se muestra');
        return null;
    }

    // Si solo hay una página, mostrar solo la información pero no los controles de navegación
    const showNavigationControls = totalPages > 1;

    return (
        <div>
            {/* Información de paginación */}
            <div className="d-flex justify-content-between align-items-center mb-3">
                <div className="pagination-info">
                    <small className="text-muted">
                        Mostrando {((currentPage - 1) * itemsPerPage) + 1} - {Math.min(currentPage * itemsPerPage, totalItems)} de {totalItems} registros
                    </small>
                </div>
                <div className="items-per-page">
                    <label className="me-2">
                        <small>Mostrar:</small>
                    </label>
                    <select
                        className="form-select form-select-sm d-inline-block w-auto"
                        value={itemsPerPage}
                        onChange={(e) => {
                            const value = Number(e.target.value);
                            console.log('Cambiando items per page a:', value);
                            onItemsPerPageChange(value);
                        }}
                    >
                        <option value="5">5</option>
                        <option value="10">10</option>
                        <option value="25">25</option>
                        <option value="50">50</option>
                        <option value="100">100</option>
                    </select>
                    <small className="ms-2">por página</small>
                </div>
            </div>

            {/* Controles de navegación - solo mostrar si hay más de una página */}
            {showNavigationControls && (
                <div className="d-flex justify-content-center mt-3">
                    <nav aria-label="Paginación de solicitantes">
                        <ul className="pagination pagination-sm">
                            {/* Botón Anterior */}
                            <li className={`page-item ${currentPage === 1 ? 'disabled' : ''}`}>
                                <button
                                    className="page-link"
                                    onClick={() => onPageChange(currentPage - 1)}
                                    disabled={currentPage === 1}
                                    aria-label="Página anterior"
                                >
                                    &laquo;
                                </button>
                            </li>

                            {/* Números de página */}
                            {(() => {
                                const pages = [];
                                const maxVisiblePages = 5;
                                let startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2));
                                let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);

                                // Ajustar el inicio si estamos cerca del final
                                if (endPage - startPage + 1 < maxVisiblePages) {
                                    startPage = Math.max(1, endPage - maxVisiblePages + 1);
                                }

                                // Primera página si no está visible
                                if (startPage > 1) {
                                    pages.push(
                                        <li key={1} className="page-item">
                                            <button className="page-link" onClick={() => onPageChange(1)}>
                                                1
                                            </button>
                                        </li>
                                    );
                                    if (startPage > 2) {
                                        pages.push(
                                            <li key="ellipsis1" className="page-item disabled">
                                                <span className="page-link">...</span>
                                            </li>
                                        );
                                    }
                                }

                                // Páginas visibles
                                for (let i = startPage; i <= endPage; i++) {
                                    pages.push(
                                        <li key={i} className={`page-item ${currentPage === i ? 'active' : ''}`}>
                                            <button
                                                className="page-link"
                                                onClick={() => onPageChange(i)}
                                                aria-label={`Página ${i}`}
                                                aria-current={currentPage === i ? 'page' : undefined}
                                            >
                                                {i}
                                            </button>
                                        </li>
                                    );
                                }

                                // Última página si no está visible
                                if (endPage < totalPages) {
                                    if (endPage < totalPages - 1) {
                                        pages.push(
                                            <li key="ellipsis2" className="page-item disabled">
                                                <span className="page-link">...</span>
                                            </li>
                                        );
                                    }
                                    pages.push(
                                        <li key={totalPages} className="page-item">
                                            <button className="page-link" onClick={() => onPageChange(totalPages)}>
                                                {totalPages}
                                            </button>
                                        </li>
                                    );
                                }

                                return pages;
                            })()}

                            {/* Botón Siguiente */}
                            <li className={`page-item ${currentPage === totalPages ? 'disabled' : ''}`}>
                                <button
                                    className="page-link"
                                    onClick={() => onPageChange(currentPage + 1)}
                                    disabled={currentPage === totalPages}
                                    aria-label="Página siguiente"
                                >
                                    &raquo;
                                </button>
                            </li>
                        </ul>
                    </nav>
                </div>
            )}
        </div>
    );
};

export default PaginationControls;
