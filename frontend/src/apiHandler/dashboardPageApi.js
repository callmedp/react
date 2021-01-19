import {fetchMyWallet} from 'store/DashboardPage/MyWallet/actions';

export const getDashboardPageActions = (params) => {
  return [
    { action: fetchMyWallet, payload: { id: params?.id } },
  ]
}

export const getDashboardPageActionsMobile = (params) => {
  return [
  ]
}



