import BaseApiService from 'services/BaseApiService';
import { siteDomain } from 'utils/domains';

const myWalletData = (data) => {
    const url = `my-wallet/?page=${data.id}`;
    return BaseApiService.get(`${siteDomain}/dashboard/api/v1/${url}`);
};


export default {
    myWalletData,
}