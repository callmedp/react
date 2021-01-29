import {fetchMyWallet} from 'store/DashboardPage/MyWallet/actions';
import {fetchMyOrders} from 'store/DashboardPage/MyOrder/actions';
import {fetchMyCourses} from 'store/DashboardPage/MyCourses/actions';
import { fetchMyServices } from 'store/DashboardPage/MyServices/actions';

export const getDashboardPageActions = (params) => {

  const actionList = {
    'mycourses': [
      { action: fetchMyCourses, payload: { page: 1 } },
    ],
    'myorder': [
      { action: fetchMyOrders, payload: { page: '1' } },
    ],
    'mywallet': [
      { action: fetchMyWallet, payload: { page: 1 } },
    ],
    'myservices': [
      { action: fetchMyServices, payload: { page: 1 } },
    ]
    }[params.name];

    return actionList ?? [];

}

export const getDashboardPageActionsMobile = (params) => {
  const actionList = {
    'mycourses': [
      { action: fetchMyCourses, payload: { page: 1 } },
    ],
    'myorder': [
      { action: fetchMyOrders, payload: { page: '1' } },
    ],
    'mywallet': [
      { action: fetchMyWallet, payload: { page: 1 } },
    ],
    'myservices': [
      { action: fetchMyServices, payload: { page: 1 } },
    ]
    }[params.name];

    return actionList ?? [];
}



