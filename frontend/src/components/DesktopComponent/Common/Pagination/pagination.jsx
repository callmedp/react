import React from 'react'

const Pagination = (props) => {
    const { total, currentPage, setCurrentPage, changePageNumber } = props;

    // console.log(setCurrentPage)

    const sortedArr = Array.apply(null, Array(total.total)).map(function (x, i) { return i+1; })

    // let half_length = Math.ceil(total.total / 2);

    return (
        <div className="db-pagination mt-20">
            { total.has_prev && sortedArr.length > 6 ? <figure className="icon-db-arrow-left" onClick={() => changePageNumber(currentPage-1)}></figure> : "" }
            { sortedArr.length <= 6 ? 
                sortedArr.map((item, idx) => {
                    return <span key={idx} className={currentPage === item ? 'active' : ""} onClick={() => changePageNumber(item)}>{item}</span>
                })
                : ""
            }

            {/* {half_length} */}
            {/* <span>1</span> <span>2</span> <span>3</span><span></span>....<span>{total.total}</span> */}
            {/* <span>1</span> <span>2</span> <span>3</span> <span className="active">4</span> <span>....</span> <span>{total.total}</span> */}
            { total.has_next && sortedArr.length > 6 ? <figure className="icon-db-arrow-right" onClick={() => changePageNumber(currentPage+1)}></figure> : "" }
        </div>
    )
}

export default Pagination;