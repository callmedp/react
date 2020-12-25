import React from "react";
import { siteDomain } from 'utils/domains';

const ProductDetails = (props) =>{
    const noOfWords = 100
    const { detailsData : { 
        about, highlights, 
        jobsAvailable,  skillList,
        url, type,level,
        brochure, u_courses_benefits }, icon, setShowDetails
    } = props

    const OpenProductPage = () =>{
        window.location.href = `${siteDomain}${url}`
    }

    return (
        <div className="m-card__popover .m-transit">
            <p className="m-type">Type: <strong>{type}</strong>  |   Course level: <strong>{level}</strong> <br />
                <strong> {jobsAvailable}</strong> Jobs available
            </p>
            
            <p className="about-ht">
                <div dangerouslySetInnerHTML={{__html: (about?.slice(noOfWords)?.length ? (about?.slice(0,noOfWords)+'...') : about?.slice(0,noOfWords))}}></div>
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

            <p className="skill-ht">
            {
                highlights &&
                <> 
                    <strong>Highlights</strong>
                    {highlights?.replace(/<[^>]*>/g, '')?.slice(80)?.length ? (highlights?.replace(/<[^>]*>/g, '')?.slice(0,80)+'...') : highlights?.replace(/<[^>]*>/g, '')?.slice(0,80)}
                </>
            }
            {
                u_courses_benefits &&
                <>
                    <strong>Highlights</strong>
                    <ul>
                        {
                            u_courses_benefits?.slice(0, 2)?.map((value, index) =>{
                                return (
                                    <li key={index}>{value}</li>
                                )
                            })
                        }
                    </ul>
                </>
            }
            </p>

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