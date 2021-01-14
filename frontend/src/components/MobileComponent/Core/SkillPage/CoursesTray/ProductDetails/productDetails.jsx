import React from "react";
import { siteDomain } from 'utils/domains';

const ProductDetails = (props) =>{
    const noOfWords = 100
    const { detailsData : { 
        about, highlights, 
        jobsAvailable,  skillList,
        url, type,level,
        brochure, u_courses_benefits, u_desc,
        number_of_questions }, icon,
        setShowDetails, productType
    } = props

    const OpenProductPage = () =>{
        window.location.href = `${siteDomain}${url}`
    }
    const regex = /<[^>]*>/g

    return (
        <div className="m-card__popover .m-transit">
            <p className="m-type">
            {
                productType === 'Assessments' ?
                !!number_of_questions ? <> Number of Questions : <strong>{number_of_questions}</strong> </>: ''
                :
                <> Type: <strong>{type}</strong>  |   Course level: <strong>{level}</strong></>
            }
                <br />
                <strong> {jobsAvailable}</strong> Jobs available
            </p>
            
            <p className="about-ht">
                {
                    u_desc ? 
                    <div dangerouslySetInnerHTML={{__html: (u_desc?.replace(regex, '').slice(noOfWords)?.length ? (u_desc?.replace(regex, '').slice(0,noOfWords)+'...') : u_desc?.replace(regex, '').slice(0,noOfWords))}}></div> :
                    <div dangerouslySetInnerHTML={{__html: (about?.replace(regex, '').slice(noOfWords)?.length ? (about?.replace(regex, '').slice(0,noOfWords)+'...') : about?.replace(regex, '').slice(0,noOfWords))}}></div> 
                }
            </p>

            <p className="skill-ht">
                { 
                    skillList && 
                    <>
                        <strong>Skills you gain</strong> 
                        { 
                            skillList?.slice(0, 5)?.map((skill, index) =>{
                                return ( 
                                    <React.Fragment key={index}>
                                        {skill}
                                        {index === skillList?.slice(0, 5).length-1 ? ' ' : '  |  '}
                                        {(skillList?.slice(0, 5)?.pop() == skill && skillList?.slice(5)?.length) ? '& Many More..' : ''}
                                    </React.Fragment>
                                )
                            })
                        }
                    </>
                } 
            </p>

            {
                productType === 'Courses' &&
                <p className="skill-ht">
                {
                    highlights?.length ? 
                    <>
                        <strong>Highlights</strong>
                        <ul>
                            {
                                highlights?.slice(0, 2)?.map((value, index) =>{
                                    return (
                                        <li key={index} dangerouslySetInnerHTML={{__html: value}}></li>
                                    )
                                })
                            }
                        </ul>
                    </> : ''
                }
                {
                    u_courses_benefits?.length ?
                    <>
                        <strong>Highlights</strong>
                        <ul>
                            {
                                u_courses_benefits?.slice(0, 2)?.map((value, index) =>{
                                    return (
                                        <li key={index} dangerouslySetInnerHTML={{__html: value}}></li>
                                    )
                                })
                            }
                        </ul>
                    </> : ''
                }
                </p>
            }

            <p className="d-flex align-items-center mt-15">
                <button type="submit" onClick={OpenProductPage} className="btn-yellow" role="button">Enroll now</button>
                { icon === 'file' ?
                    (brochure ? <a href={brochure} className="micon-pdf ml-auto"></a> : '') : 
                    <span className="m-view-less d-block text-right ml-auto" onClick={()=>setShowDetails(false)}>View less</span>
                }
            </p>
        </div>
    )
}

export default ProductDetails;