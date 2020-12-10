import React, { useEffect } from 'react';
import './banner.scss';
import Breadcrumb from 'react-bootstrap/Breadcrumb';
import Carousel from 'react-bootstrap/Carousel';
import { useDispatch, useSelector } from 'react-redux';
import { fetchSkillPageBanner } from 'store/SkillPage/Banner/actions';
import { siteDomain } from 'utils/domains'; 

const BannerSkill = (props) => {
    
    const dispatch = useDispatch()
    const { name, breadcrumbs, featuresList } = useSelector( store => store.skillBanner )
    const pageId = props.pageId
    
    useEffect(() => {
        dispatch(fetchSkillPageBanner({id : pageId, 'medium': 0}))
    },[pageId])



    return (
       <header className="container-fluid pos-rel">
           <figure className="banner-img row">
                <img src="/media/images/home-bg.svg" alt="Digital Marketing Courses & Certifications" />
            </figure>
            <div className="container header-content">
                <div className="row">
                    <Breadcrumb>
                        {
                            breadcrumbs?.map((bread, index) => {
                                if(!!bread.url)
                            return (<Breadcrumb.Item key={index} href={`${siteDomain}${bread.url}`} >{bread.name}</Breadcrumb.Item>)
                                else
                            return (<Breadcrumb.Item key={index} >{bread.name}</Breadcrumb.Item> )
                            })
                        }
                    </Breadcrumb>
                    <h1 className="heading1">
                        { name } Courses & Certifications
                    </h1>
                    <Carousel className="header-carousel">
                        {
                            featuresList?.map((feature, index) => {
                                return (
                                    <Carousel.Item key={index} >
                                        <p key={Math.random()}>
                                            <figure className="icon-round-arrow"></figure>
                                            <span className="flex-1">{ feature }</span>
                                        </p>
                                    </Carousel.Item>
                                )
                            })
                        }
                    </Carousel>
                </div>
            </div>
       </header> 
    )
}

export default BannerSkill;