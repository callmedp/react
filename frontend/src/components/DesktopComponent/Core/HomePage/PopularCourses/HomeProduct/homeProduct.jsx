import React, { useState } from 'react';
import Carousel from 'react-bootstrap/Carousel';
import { Link } from 'react-router-dom';
import { useDispatch } from "react-redux";
import { fetchInDemandProducts } from 'store/HomePage/actions';
import { startHomePageLoader, stopHomePageLoader } from 'store/Loader/actions';
import { siteDomain } from 'utils/domains';

const HomeProduct = (props) => {
  
    const [index, setIndex] = useState(0);
    const { tabType, popularProducts } = props;
    const dispatch = useDispatch()

    const handleSelect = async (selectedIndex, e) => {
        if (e !== undefined) {
            if (popularProducts.length === 0 || popularProducts[selectedIndex].length === 0) {
                dispatch(startHomePageLoader())
                await new Promise((resolve, reject) => dispatch(fetchInDemandProducts({ payload: {pageId: selectedIndex + 1, tabType, device: 'desktop'}, resolve, reject })));
                dispatch(stopHomePageLoader())
            }
            setIndex(selectedIndex);
        }
    };

    const starRatings = (star, index) => {
        return (star === '*' ? <em className="icon-fullstar" key={index}></em> : star === '+'
            ? <em className="icon-halfstar" key={index}></em> : <em className="icon-blankstar" key={index}></em>
        )
    }
   



    return (
        <Carousel className="" fade={true} activeIndex={index} onSelect={handleSelect} >
            {
                popularProducts?.map((productList, indx) => {
                    
                    return (
                        <Carousel.Item interval={10000000000} key={indx}>
                            <ul className="courses-tray__list">
                                {
                                    productList?.map((product, idx) => {
                                        return (
                                            <li className="col-sm-3" key={product.id}>
                                                <div className="card">
                                                    <div className={`card__heading colbg${idx+1}`}>
                                                        {product.tags === 2 && <span className="flag-blue1">NEW</span>}
                                                        {product.tags === 1 && <span className="flag-yellow">BESTSELLER</span>}
                                                        <figure>
                                                            <img src={product.imgUrl} alt={product.imageAlt} itemProp="image" />
                                                        </figure>
                                                        <h3 className="heading3">
                                                            <a itemProp="url" href={`${product.url}`} >{product.name}</a>
                                                        </h3>
                                                    </div>
                                                    <div className="card__box">
                                                        <div className="card__rating mt-5">
                                                            <span className="rating">
                                                                {product.stars?.map((star, index) => starRatings(star, index))}
                                                                <span>{product.rating?.toFixed(1)}/5</span>
                                                            </span>
                                                            {product.mode ? <span className="mode">{product.mode}</span> : ''}
                                                        </div>
                                                        <div className="card__duration-mode mt-10">
                                                            {product.jobsAvailable ? <> <strong>{product.jobsAvailable}</strong> Jobs available </> : ''} {product.jobsAvailable && product.duration ? '|' : ''} {product.duration ? <>Duration: <strong>{product.duration} days</strong> </> : <strong>&nbsp;</strong>}
                                                        </div>
                                                        <a className="view-program mt-10" href={`${siteDomain}${product.url}`}>View program</a>
                                                    </div>
                                                </div>
                                            </li>
                                        )
                                    })
                                }
                            </ul>
                        </Carousel.Item>
                    )
                })
            }
        </Carousel>
    )
}

export default HomeProduct;









// [
//     [
//       {
//         id: 4,
//         name: 'Profile plus package',
//         about: 'Certified Logistics and Supply Chain Professional Logistics and Supply Chain Management Professional Certification, offered by Vskills, approved by Government (PSU) helps in to enhancing traditional management by focusing on organization and integration amongst various partners of supply.',
//         url: '/course/category21-2/profile-plus-package/pd-4',
//         imgUrl: 'https://learning-media-staging-189607.storage.googleapis.com/l1/m/product_image/4/1591342088_9121.png',
//         imgAlt: 'Profile plus package',
//         title: 'Profile plus package (INR 1) - Shine Learning',
//         slug: 'profile-plus-package',
//         jobsAvailable: 4,
//         skillList: [Array],
//         rating: 3,
//         stars: [Array],
//         mode: null,
//         providerName: 'Career Plus',
//         price: 1,
//         tags: 2,
//         highlights: [Array],
//         brochure: null,
//         u_courses_benefits: null,
//         u_desc: '<p>Why should one take this certificate? It is used to develop knowledge, skills and competencies in the field of Logistics &amp; Supply Chain Management so as to learn different aspects of logistics including purchase, operations, warehouse, transportation and supply chain management. This certificate assists one in understanding logistics and supply chain management globally</p>'
//       },
//       {
//         id: 1,
//         name: 'Lean Six Sigma Green Belt Test',
//         about: 'Test GreyCampus offers an online training and certification program on Lean Six Sigma Green Belt. Study with confidence as the course covers every topic in accordance with IASSC. Lean Six Sigma incorporates the most widely-used concepts and tools from both the Lean and Six Sigma bodies of knowledge along with DMAIC problem solving approach.',
//         url: '/course/courses-certifications/lean-six-sigma-green-belt-test/pd-1',
//         imgUrl: 'https://learning-media-staging-189607.storage.googleapis.com/l2/m/product_image/1/1608784815_5352.png',
//         imgAlt: 'Lean Six Sigma Green Belt',
//         title: 'Lean Six Sigma Green Belt Test (INR 500) - Shine Learning',
//         slug: 'lean-six-sigma-green-belt-test',
//         jobsAvailable: 555,
//         skillList: [Array],
//         rating: 4.93,
//         stars: [Array],
//         mode: 'Online',
//         providerName: 'Career Plus',
//         price: 100,
//         tags: 2,
//         highlights: [Array],
//         brochure: null,
//         u_courses_benefits: null,
//         u_desc: '<ul>\n' +
//           '\t<li>Lean Best suited for candidates who wish to make a successful career in quality function of an organization. management, communication, adaptability, leadership, time management, ruby on rails, react, angular, vue, decision making, communication, mongodb, ruby on rails, decision making, who, six sigma, time management</li>\n' +
//           '</ul>\n' +
//           '\n' +
//           '<p>&nbsp;</p>',
//         duration: 100,
//         type: 'Basic + More Deliverable',
//         label: 'course 3',
//         level: 'Advanced'
//       },
//       {
//         id: 11,
//         name: 'Six Sigma Black Beltsssss',
//         about: 'Certified Logistics and Supply Chain Professional Logistics and Supply Chain Management Professional Certification, offered by Vskills, approved by Government (PSU) helps in to enhancing traditional management by focusing on organization and integration amongst various partners of supply chain for better management; thus providing greater value to the consumer. Certified professionals find employment in various means',
//         url: '/course/sales-and-marketing/six-sigma-black-beltsssss/pd-11',
//         imgUrl: 'https://learning-media-staging-189607.storage.googleapis.com/l1/m/product_image/11/1608007670_5453.jpg',
//         imgAlt: 'Six Sigma Black Belt',
//         title: 'Six Sigma Black Belts (INR 1) - Shine Learning',
//         slug: 'six-sigma-black-beltsssss',
//         jobsAvailable: 23923,
//         skillList: [Array],
//         rating: 4.91,
//         stars: [Array],
//         mode: 'Online',
//         providerName: 'VSkill',
//         price: 1,
//         tags: 0,
//         highlights: [Array],
//         brochure: null,
//         u_courses_benefits: null,
//         u_desc: '<p>Why should one take this certificate? It is used to develop knowledge, skills and competencies in the field of Logistics &amp; Supply Chain Management so as to learn different aspects of logistics including purchase, operations, warehouse, transportation and supply chain management. This certificate assists one in understanding logistics and supply chain management globally</p>',
//         duration: 180,
//         type: 'Basic + More Deliverable',
//         label: 'Six Sigma Black Beltsssss',
//         level: 'Beginner'
//       },
//       {
//         id: 1589,
//         name: ' Advanced Solutions of MS SharePoint Server 2013 Online Training',
//         about: '\n' +
//           'Universally recognized course\n' +
//           'Clear picture of all domains of SharePoint Server 2013\n' +
//           'Good understanding of organizing, cooperating and allocating information in the organization\n' +
//           'Scope for better opportunities\n',
//         url: '/course/operation-management/advanced-solutions-of-ms-sharepoint-server-2013-online-training/pd-1589',
//         imgUrl: 'https://learning-media-staging-189607.storage.googleapis.com/l1/m/attachment/default_product_image.jpg',
//         imgAlt: ' Advanced Solutions of MS SharePoint Server 2013 Online Training',
//         title: ' Advanced Solutions of MS SharePoint Server 2013 Online Training -  (INR 3099) - Shine Learning',
//         slug: 'advanced-solutions-of-ms-sharepoint-server-2013-online-training',
//         jobsAvailable: 64345,
//         skillList: null,
//         rating: 4.5,
//         stars: [Array],
//         mode: null,
//         providerName: 'simplilearn',
//         price: 3099,
//         tags: 0,
//         highlights: [Array],
//         brochure: null,
//         u_courses_benefits: null,
//         u_desc: `<p class="MsoNormal" style="margin-bottom: 0.0001pt; text-align: justify;"><span style="font-size: 10.0pt; font-family: 'Verdana','sans-serif';">The course provided by Simplilearn focuses on giving a clear picture of MS SharePoint Server 2013. After the completion of the course, a candidate will be able to distinct easily among business connectivity services and business intelligence solutions.</span></p>\n` +
//           `<p class="MsoNormal" style="margin-bottom: 0.0001pt; text-align: justify;"><span style="font-size: 10.0pt; font-family: 'Verdana','sans-serif';">With Shine.com, you get one month complimentary Featured Profile services which further gives boost to your job search and chances of recruiter view increases by 10 times.</span></p>`,
//         duration: 0,
//         type: '',
//         label: ' Advanced Solutions of MS SharePoint Server 2013 Online Training',
//         level: ''
//       }
//     ],
//     {
//       id: 1,
//       name: 'Lean Six Sigma Green Belt Test',
//       about: 'Test GreyCampus offers an online training and certification program on Lean Six Sigma Green Belt. Study with confidence as the course covers every topic in accordance with IASSC. Lean Six Sigma incorporates the most widely-used concepts and tools from both the Lean and Six Sigma bodies of knowledge along with DMAIC problem solving approach.',
//       url: '/course/courses-certifications/lean-six-sigma-green-belt-test/pd-1',
//       imgUrl: 'https://learning-media-staging-189607.storage.googleapis.com/l2/m/product_image/1/1608784815_5352.png',
//       imgAlt: 'Lean Six Sigma Green Belt',
//       title: 'Lean Six Sigma Green Belt Test (INR 500) - Shine Learning',
//       slug: 'lean-six-sigma-green-belt-test',
//       jobsAvailable: 555,
//       skillList: [
//         'CSS',                   'Java',
//         'Python',                'MongoDB',
//         'Javascript',            'Time Management',
//         'Management',            'Communication',
//         'LEAN',                  'Six Sigma',
//         'Data Structures',       'Ruby On Rails',
//         'Selenium',              'Spooler Plus',
//         'GST',                   'Energy Efficiency',
//         'Efficiency Management', 'Production',
//         'Production Techniques', 'Vcs Simulator',
//         'Loop Simulator',        'ios',
//         'aol',                   'Decision Making',
//         'WHO',                   'A++',
//         'Adaptability'
//       ],
//       rating: 4.93,
//       stars: [ '*', '*', '*', '*', '*' ],
//       mode: 'Online',
//       providerName: 'Career Plus',
//       price: 100,
//       tags: 2,
//       highlights: [
//         'Test GreyCampus offers an online training and certification program on Lean Six Sigma Green Belt.',
//         'Study with confidence as the course covers every topic in accordance with IASSC.'
//       ],
//       brochure: null,
//       u_courses_benefits: null,
//       u_desc: '<ul>\n' +
//         '\t<li>Lean Best suited for candidates who wish to make a successful career in quality function of an organization. management, communication, adaptability, leadership, time management, ruby on rails, react, angular, vue, decision making, communication, mongodb, ruby on rails, decision making, who, six sigma, time management</li>\n' +
//         '</ul>\n' +
//         '\n' +
//         '<p>&nbsp;</p>',
//       duration: 100,
//       type: 'Basic + More Deliverable',
//       label: 'course 3',
//       level: 'Advanced'
//     },
//     {
//       id: 11,
//       name: 'Six Sigma Black Beltsssss',
//       about: 'Certified Logistics and Supply Chain Professional Logistics and Supply Chain Management Professional Certification, offered by Vskills, approved by Government (PSU) helps in to enhancing traditional management by focusing on organization and integration amongst various partners of supply chain for better management; thus providing greater value to the consumer. Certified professionals find employment in various means',
//       url: '/course/sales-and-marketing/six-sigma-black-beltsssss/pd-11',
//       imgUrl: 'https://learning-media-staging-189607.storage.googleapis.com/l1/m/product_image/11/1608007670_5453.jpg',
//       imgAlt: 'Six Sigma Black Belt',
//       title: 'Six Sigma Black Belts (INR 1) - Shine Learning',
//       slug: 'six-sigma-black-beltsssss',
//       jobsAvailable: 23923,
//       skillList: [ 'HTML', 'CSS', 'Python', 'DJANGO', 'GST', 'Production' ],
//       rating: 4.91,
//       stars: [ '*', '*', '*', '*', '*' ],
//       mode: 'Online',
//       providerName: 'VSkill',
//       price: 1,
//       tags: 0,
//       highlights: [
//         'Certified Logistics and Supply Chain Professional Logistics and Supply Chain Management Professional Certification, offered by Vskills, approved by Government (PSU) helps in to enhancing traditional management by focusing on organization and integration amongst various partners of supply chain for better management; thus providing greater value to the consumer.'
//       ],
//       brochure: null,
//       u_courses_benefits: null,
//       u_desc: '<p>Why should one take this certificate? It is used to develop knowledge, skills and competencies in the field of Logistics &amp; Supply Chain Management so as to learn different aspects of logistics including purchase, operations, warehouse, transportation and supply chain management. This certificate assists one in understanding logistics and supply chain management globally</p>',
//       duration: 180,
//       type: 'Basic + More Deliverable',
//       label: 'Six Sigma Black Beltsssss',
//       level: 'Beginner'
//     },
//     {
//       id: 1589,
//       name: ' Advanced Solutions of MS SharePoint Server 2013 Online Training',
//       about: '\n' +
//         'Universally recognized course\n' +
//         'Clear picture of all domains of SharePoint Server 2013\n' +
//         'Good understanding of organizing, cooperating and allocating information in the organization\n' +
//         'Scope for better opportunities\n',
//       url: '/course/operation-management/advanced-solutions-of-ms-sharepoint-server-2013-online-training/pd-1589',
//       imgUrl: 'https://learning-media-staging-189607.storage.googleapis.com/l1/m/attachment/default_product_image.jpg',
//       imgAlt: ' Advanced Solutions of MS SharePoint Server 2013 Online Training',
//       title: ' Advanced Solutions of MS SharePoint Server 2013 Online Training -  (INR 3099) - Shine Learning',
//       slug: 'advanced-solutions-of-ms-sharepoint-server-2013-online-training',
//       jobsAvailable: 64345,
//       skillList: null,
//       rating: 4.5,
//       stars: [ '*', '*', '*', '*', '+' ],
//       mode: null,
//       providerName: 'simplilearn',
//       price: 3099,
//       tags: 0,
//       highlights: [
//         'Training for Advanced Solutions of Microsoft SharePoint Server 2013 Exam 70-332',
//         '10 High Quality e-Learning Chapters'
//       ],
//       brochure: null,
//       u_courses_benefits: null,
//       u_desc: `<p class="MsoNormal" style="margin-bottom: 0.0001pt; text-align: justify;"><span style="font-size: 10.0pt; font-family: 'Verdana','sans-serif';">The course provided by Simplilearn focuses on giving a clear picture of MS SharePoint Server 2013. After the completion of the course, a candidate will be able to distinct easily among business connectivity services and business intelligence solutions.</span></p>\n` +
//         `<p class="MsoNormal" style="margin-bottom: 0.0001pt; text-align: justify;"><span style="font-size: 10.0pt; font-family: 'Verdana','sans-serif';">With Shine.com, you get one month complimentary Featured Profile services which further gives boost to your job search and chances of recruiter view increases by 10 times.</span></p>`,
//       duration: 0,
//       type: '',
//       label: ' Advanced Solutions of MS SharePoint Server 2013 Online Training',
//       level: ''
//     }
//   ]
  

