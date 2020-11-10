import React from 'react';
import './banner.scss';
import Breadcrumb from 'react-bootstrap/Breadcrumb'

const BannerSkill = (props) => {
    return (
       <header className="container-fluid">
           <figure className="banner-img row">
                <img src="./media/images/home-bg.svg" alt="" />
            </figure>
            <div className="container header-content">
                <div className="row">
                    <Breadcrumb>
                        <Breadcrumb.Item href="#">Home</Breadcrumb.Item>
                        <Breadcrumb.Item href="#">
                            Sales and Marketing
                        </Breadcrumb.Item>
                        <Breadcrumb.Item active>Digital Marketing</Breadcrumb.Item>
                    </Breadcrumb>
                    <h1>
                        Digital Marketing Courses & Certifications
                    </h1>
                    <p>
                        <i className="icon-round-arrow"></i>
                        Digital Marketing expected to <strong>create 3.3 million jobs by 2022</strong>
                    </p>
                </div>
            </div>
       </header> 
    )
}

export default BannerSkill;