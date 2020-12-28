import BaseApiService from 'services/BaseApiService'

import { siteDomain } from 'utils/domains'


const coursesAndAssessments = (data) => {
    const url = `courses-and-assessments/?id=${data?.id}`;

    return BaseApiService.get(`${siteDomain}/courses/api/v1/${url}`);
};


export default {
    coursesAndAssessments,
}