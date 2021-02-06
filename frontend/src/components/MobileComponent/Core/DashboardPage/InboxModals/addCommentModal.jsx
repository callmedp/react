import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useForm } from "react-hook-form";
import Swal from 'sweetalert2';
import { fetchOiComment } from 'store/DashboardPage/AddSubmitComment/actions/index';
import inboxForm from 'formHandler/mobileFormHandler/formData/inboxForm';
import { TextArea } from 'formHandler/mobileFormHandler/formFields';
import { startCommentLoader, stopCommentLoader } from 'store/Loader/actions/index';
import Loader from '../../../Common/Loader/loader';
import { updateServiceCommentCount } from 'store/DashboardPage/MyServices/actions/index';
import { updateCourseCommentCount } from 'store/DashboardPage/MyCourses/actions/index';

const AddCommentModal = (props) => {
    const { setShowCommentModal, oi_id, type } = props
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
        let response = await new Promise((resolve, reject) => dispatch(fetchOiComment({ payload: new_values, resolve, reject })));
        dispatch(stopCommentLoader());
        reset();
        Swal.fire({
            icon: 'success',
            text: 'Comment sent successfully !'
        })
        if (response?.error) {
            Swal.fire({
                title: response?.error,
                type: 'error'
            })
        }
        else {
            if(type === "myservices"){
                dispatch(updateServiceCommentCount({ id: response.oi_id, no_of_comments: response.comment.length}));
            }
            else{
                dispatch(updateCourseCommentCount({ id: response.oi_id, no_of_comments: response.comment.length}));
            }
        }
        setShowCommentModal(false)
    };

    const handleEffects = async () => {
        let commVal = {
            oi_id: oi_id,
            type: 'GET'
        }
        try {

            dispatch(startCommentLoader());
            await new Promise((resolve, reject) => dispatch(fetchOiComment({ payload: commVal, resolve, reject })));
            dispatch(stopCommentLoader());

        }
        catch (e) {
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
                <span className="m-db-close" onClick={() => { setShowCommentModal(false) }}>X</span>
                {comments?.length ? <><br /><br /></> : ''}
                <div className="">
                    {
                        comments?.length ?
                            <>
                                <ul className="m-timeline-list">
                                    {
                                        comments?.map((comment, idx) => {
                                            return (
                                                <li key={idx}>
                                                    <i className="m-timeline-list--dot"></i>
                                                    <span>{comment.created} {comment.addedBy ? '   |   By ' + comment.added_by : ""} </span>
                                                    <p className="m-timeline-list--text">{comment?.message}</p>
                                                </li>
                                            )
                                        })
                                    }
                                </ul>
                                <hr />
                            </> : ''
                    }
                    <form onSubmit={handleSubmit(submitComment)}>
                        <div className="m-enquire-now mt-15 text-center">
                            {/* <span className="error_cls">
                                {errors.comment && "* Please write something to post comment."}
                            </span><br /> */}
                            <h2>Add Comment</h2><br />
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