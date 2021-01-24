import { siteDomain } from '../domains'
import { getDataStorage } from '../storage'

const downloadInvoice = (orderId) => {
    const url = `${siteDomain}/api/v1/download-invoice/?candidate_id=${getDataStorage('candidate_id')}&email=${getDataStorage('email')}&order_pk=${orderId}`;
    return url;
};

const getPaginationList = (startPage, totalPage) => {
    var pageList = []
    var endPage = (totalPage < 6) ? (totalPage + 1) : ((startPage + 6) > totalPage ? (totalPage + 1) : (startPage + 6))

    for (let x = startPage; x < endPage; x++)
        pageList.push(x);

    if(pageList[pageList.length - 1] !== totalPage){
        pageList.pop();
        pageList.pop();
        pageList.push('....')
        pageList.push(totalPage)
    }
    return pageList
}

export {
    downloadInvoice,
    getPaginationList
}