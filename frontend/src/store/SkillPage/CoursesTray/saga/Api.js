import BaseApiService from 'services/BaseApiService'

import { siteDomain } from 'utils/domains'
import { CountryCode2 } from 'utils/storage';


const coursesAndAssessments = (data) => {
    const code2 = CountryCode2() || data?.code2 || 'IN';
    const url = `courses-and-assessments/?id=${data?.id}&code2=${code2}`;

    return BaseApiService.get(`${siteDomain}/courses/api/v1/${url}`);
};


export default {
    coursesAndAssessments,
}