import { createAction } from '@reduxjs/toolkit';

const fetchLeadManagement = createAction('FETCH_LEAD_MANAGEMENT');
const leadManagementFetched = createAction('LEAD_MANAGEMENT_FETCHED');

export {
    fetchLeadManagement,
    leadManagementFetched,
}