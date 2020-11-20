import BaseApiService from 'services/BaseApiService'

import { siteDomain } from 'utils/domains'

var data = {'pCourseList': [{
    name: 'Email Marketing Master Training Course',
    id: '1',
    img : 'https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png',
    alt : 'Digital Marketing Training Course',
    ratings : '4',
    stars : ['*', '*', '*', '*'],
    url : 'https://learning.shine.com'
},
{
    name: 'Email Marketing Master Training Course',
    id: '2',
    img : 'https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png',
    alt : 'Digital Marketing Training Course',
    ratings : '4',
    stars : ['*', '*', '*', '*'],
    url : 'https://learning.shine.com'
},
{
    name: 'Email Marketing Master Training Course',
    id: '3',
    img : 'https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png',
    alt : 'Digital Marketing Training Course',
    ratings : '4',
    stars : ['*', '*', '*', '*'],
    url : 'https://learning.shine.com'
}]}
const populerCourses = () => {
    // const url = ``;
    // return BaseApiService.get(``);
    return {'data': data}
};

export default {
    populerCourses,
}