import React from 'react'
import { getPaginationList } from 'utils/dashboardUtils/myOrderUtils'
import { useState } from 'react'

const Pagination = (props) => {
    const { totalPage, currentPage, setCurrentPage } = props;
    const [startPage, setStartPage] = useState(1);
    const paginationList = getPaginationList(startPage, totalPage);
    const length = paginationList?.length;

    const getPrev = () => {
        !paginationList.includes(currentPage - 1) &&
            setStartPage(currentPage - 4);
            setCurrentPage(currentPage - 1)
        }

    const getNext = () => {
        !paginationList.includes(currentPage + 1) &&
            setStartPage(currentPage + 1);
            setCurrentPage(currentPage + 1)
    }

    return (
        <div className="m-db-pagination mt-20">
            { startPage > 1 && <figure className="icon-db-arrow-left" onClick={getPrev} /> }
            {
                paginationList?.map((item, i) => {
                    return <span key={i} className={ item === currentPage ? 'active' : '' } onClick={() => { item !== '....' && setCurrentPage(item)}}>{item}</span>
                })
            }
            { 
                paginationList[length -2] === '....' &&
                paginationList[length -1] === totalPage &&
                    <figure className="icon-db-arrow-right" onClick={getNext} />
            }
        </div>
    )
}

export default Pagination;