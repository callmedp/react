import {fetchMyWallet} from 'store/DashboardPage/MyWallet/actions';
import {fetchMyOrders} from 'store/DashboardPage/MyOrder/actions';
import {fetchMyCourses} from 'store/DashboardPage/MyCourses/actions';

export const getDashboardPageActions = (params) => {
  return [
    { action: fetchMyWallet, payload: { id: params?.id } },
    { action: fetchMyOrders, payload: { id: params?.id } },
    { action: fetchMyCourses, payload: { } },
  ]
}

export const getDashboardPageActionsMobile = (params) => {
  return [
  ]
}



