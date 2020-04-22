import { siteDomain } from '../../../Utils/domains';
export const menuData = [
    {
        label : 'Home',
        url: '/resume-score-checker',
        icon: 'icon-home'
    },
    {
        label : 'Courses',
        url: `${siteDomain}`,
        icon: 'icon-courses'
    },
    {
        label : 'Job Assistance',
        url: "https://learning.shine.com/services/resume-writing/63/",
        icon: 'job-assistance'
    },
    {
        label : 'Practice Tests',
        url: `${siteDomain}/practice-tests/`,
        icon: 'practice-tests'
    },
    {
        label : 'Free Resources',
        url: `${siteDomain}/cms/resume-format/1/`,
        icon: 'free-resources'
    },
    {
        label : 'Blog',
        url: `${siteDomain}/talenteconomy/`,
        icon: 'blog'
    },
]

export default menuData;