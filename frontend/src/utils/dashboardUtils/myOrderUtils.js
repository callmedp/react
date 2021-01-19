import { siteDomain } from '../domains'

const downloadInvoice = (orderId) => {
    const url = `${siteDomain}/api/v1/download-invoice/?candidate_id=''&email=''&order_pk=${orderId}`;
    return url;
};

export {
    downloadInvoice,
}