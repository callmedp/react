import React, { useState } from 'react';
import './courseEnrol.scss';
import {Link} from 'react-router-dom';
import { getStudyMode } from 'utils/detailPageUtils/studyMode';


const CourseEnrol = (props) => {
    const { product_detail } = props
    // console.log(product_detail)
    const [varChecked, changeChecked] = useState({});

    // const changeMode = (objj) => {
    //     let selectedObj = objj;
    //     changeChecked({...selectedObj});
    // }

    return (
        <section className="m-container mt-80n mb-0 pb-0">
            <div className="m-course-enrol">
                <div className="m-course-enrol__mode"> 
                    <form>
                        <strong>Mode</strong>
                        {
                            product_detail?.var_list?.map((varList) => {
                                return (
                                    <label key={varList.id}>
                                        <input type="radio" value="" /> {getStudyMode(varList?.mode)}
                                    </label>
                                )
                            })
                        }
                        {/* <label><input type="radio" value="" defaultChecked /> Online</label> 
                        <label><input type="radio" value="" /> Classroom</label> */}
                    </form>
                </div>
                <div className="m-course-enrol__price">
                    <strong className="mt-20 mb-10">{varChecked?.inr_price || product_detail?.var_list[0]?.inr_price}/- <del>{product_detail?.start_price}-</del></strong>
                    <Link to={"#"} className="btn btn-secondary mt-10 ml-auto">Enroll now</Link>
                </div>
                <div className="m-course-enrol__offer lightblue-bg2">
                    <strong className="mt-10 mb-5">Offers</strong>
                    <ul className="pb-0">
                        <li><figure className="micon-offer-pay"></figure> Buy now & <strong>pay within 14 days using ePayLater</strong> </li>
                        <li><figure className="micon-offer-test"></figure> Take <strong>free practice test</strong> to enhance your skill</li>
                        <li><figure className="micon-offer-badge"></figure> <strong>Get badging</strong> on your Shine profile</li>
                        <li><figure className="micon-offer-global"></figure> <strong>Global</strong> Education providers</li>
                    </ul>
                    <Link to={"#"}>+2 more</Link>
                </div>
            </div>
        </section>
    )
}

export default CourseEnrol;