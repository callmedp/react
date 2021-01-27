import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useForm } from "react-hook-form";
import Swal from 'sweetalert2';
import { fetchOiComment } from 'store/DashboardPage/AddSubmitComment/actions/index';
import inboxForm from 'formHandler/mobileFormHandler/formData/inboxForm';
import { TextArea } from 'formHandler/mobileFormHandler/formFields';
import { startCommentLoader, stopCommentLoader } from 'store/Loader/actions/index';
import Loader from '../../../Common/Loader/loader';

const AddCommentModal = (props) => {
    const { setShowCommentModal, oi_id }  = props
    const dispatch = useDispatch();
    const comments = useSelector(store => store?.getComment?.comment);
    const { commentLoader } = useSelector(store => store.loader);
    const { register, handleSubmit, errors, reset } = useForm();

    const submitComment = async values => {
        const new_values = {
          ...values,
          oi_pk: oi_id,
          type: "POST",
        };

        dispatch(startCommentLoader());
        let addedComment = await new Promise((resolve, reject) => dispatch(fetchOiComment({payload: new_values, resolve, reject })));
        dispatch(stopCommentLoader());
        reset(addedComment);
        Swal.fire({
            icon: 'success',
            text: 'Comment sent successfully !'
        })
        setShowCommentModal(false)
    };

    const handleEffects = async () => {
        let commVal = {
            oi_id: oi_id,
            type: 'GET'
        }
        try{
            if (!(window && window.config && window.config.isServerRendered)) {
                dispatch(startCommentLoader());
                await new Promise((resolve, reject) => dispatch(fetchOiComment({payload: commVal, resolve, reject })));
                dispatch(stopCommentLoader());
            }
            else {
                delete window.config?.isServerRendered
            }
        }
        catch(e){
            dispatch(stopCommentLoader());
            Swal.fire({
                icon: 'error',
                text: 'Sorry! we are unable to fecth your data.'
            })
        }
    };

    useEffect(() => {
        handleEffects();
    }, [oi_id])

    return (
        <>
            { commentLoader && <Loader />}
            <div className="m-slide-modal">
                <span className="m-db-close" onClick={() => {setShowCommentModal(false)}}>X</span>
                { comments?.length ? <><br /><br /></> : ''}
                <div className="">
                {
                    comments?.length ?
                        <>
                        <ul className="m-timeline-list">
                            {
                                comments?.map((comment, idx) => {
                                    return(
                                        <li key={idx}>
                                            <i className="m-timeline-list--dot"></i>
                                            <span>{comment.created} {comment.addedBy ?  '   |   By ' + comment.added_by : ""} </span>
                                            <p className="m-timeline-list--text">{comment?.message}</p>
                                        </li>
                                    )
                                })
                            }
                            {/* <li>
                                <i className="m-timeline-list--dot"></i>
                                <span>Dec. 11, 2020    |   By Amit Kumar</span>
                                <p className="m-timeline-list--text">Need help to understand this service.</p>
                            </li>
                            
                            <li>
                                <i className="m-timeline-list--dot"></i>
                                <span>Dec. 12, 2020    |   By Sumit Sharme</span>
                                <p className="m-timeline-list--text">We will call you for detailed info of this service</p>
                            </li>
                            
                            <li>
                                <i className="m-timeline-list--dot"></i>
                                <span>Dec. 18, 2020    |   By Amit Kumar</span>
                                <p className="m-timeline-list--text">Thanks for your confirmation!</p>
                            </li>
                            <li>
                                <i className="m-timeline-list--dot"></i>
                                <span>Dec. 11, 2020    |   By Amit Kumar</span>
                                <p className="m-timeline-list--text">Need help to understand this service.</p>
                            </li>
                            
                            <li>
                                <i className="m-timeline-list--dot"></i>
                                <span>Dec. 12, 2020    |   By Sumit Sharme</span>
                                <p className="m-timeline-list--text">We will call you for detailed info of this service</p>
                            </li>
                            
                            <li>
                                <i className="m-timeline-list--dot"></i>
                                <span>Dec. 18, 2020    |   By Amit Kumar</span>
                                <p className="m-timeline-list--text">Thanks for your confirmation!</p>
                            </li> */}
                        </ul>
                        <hr />
                        </> : ''
                }
                    <form onSubmit={handleSubmit(submitComment)}>
                        <div className="m-enquire-now mt-15 text-center">
                            <div className="m-form-group">
                                <TextArea attributes={inboxForm.name} register={register} errors={!!errors ? errors[inboxForm.name.name] : ''} />
                            </div>
                            <button className="btn btn-blue" onClick={handleSubmit(submitComment)}>Submit</button>
                        </div>
                    </form>
                </div>

            </div>
        </>
    )
}

export default AddCommentModal