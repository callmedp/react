import React from 'react'

const Pagination = (props) => {
    const { 
        totalPage, currentPage, setCurrentPage
    } = props

    return (
        <div className="m-db-pagination mt-20">
            <figure className="icon-db-arrow-left"></figure>
            <span>1</span> <span>2</span> <span>3</span> <span className="active">4</span> <span>....</span> <span>9</span>
            <figure className="icon-db-arrow-right"></figure>
        </div>
    )
}

export default Pagination;