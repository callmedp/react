import React from "react";
import { siteDomain } from 'utils/domains';

const ProductDetails = (props) =>{
    const { detailsData : { 
        about, highlights, 
        jobsAvailable,  skillList,
        url, type,level,
        brochure }, icon, setShowDetails
    } = props

    const OpenProductPage = () =>{
        window.location.replace(`${siteDomain}${url}`)
    }

    return (
        <div className="m-card__popover .m-transit">
            <p className="m-type">Type: <strong>{type}</strong>  |   <strong>Course level:</strong> {level} 
                <strong> {jobsAvailable}</strong> Jobs available
            </p>
            
            <p>
                <strong>About</strong>
                {about}
            </p>

            {skillList? <p>
                <strong>Skills you gain</strong> 
                { 
                    skillList?.map((skill, index) =>{
                        return ( 
                            <React.Fragment key={index}>
                                {skill}
                                {index === skillList.length-1 ? '' : '  |  '}
                            </React.Fragment>
                        )
                    })
                } 
            </p>: null }

            {highlights?<p>
                <strong>Highlights</strong>
                {/* <ul>
                    <li>Anytime and anywhere access</li>
                    <li>Become a part of Job centre</li>
                    <li>Lifetime course access</li>
                    <li>Access to online e-learning</li>
                </ul> */}
                <p dangerouslySetInnerHtml={{__html : highlights}}></p>
            </p>: null }

            <p className="d-flex align-items-center">
                <button type="submit" onClick={OpenProductPage} className="btn-yellow" role="button">Enroll now</button>
                { icon === 'file' ?
                    <a href={brochure} className="micon-pdf ml-auto"></a> : 
                    <span className="m-view-less d-block text-right" onClick={()=>setShowDetails(false)}>View less</span>
                }
            </p>
        </div>
    )
}

export default ProductDetails;