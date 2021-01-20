import { siteDomain } from '../domains'
import { getDataStorage } from '../storage'

const downloadInvoice = (orderId) => {
    const url = `${siteDomain}/api/v1/download-invoice/?candidate_id=${getDataStorage('candidate_id')}&email=${getDataStorage('email')}&order_pk=${orderId}`;
    return url;
};

export {
    downloadInvoice,
}