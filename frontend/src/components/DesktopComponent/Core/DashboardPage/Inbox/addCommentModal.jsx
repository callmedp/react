import React, { useEffect, useState } from 'react';
import { Collapse } from 'react-bootstrap';
import { useForm } from "react-hook-form";
import {getCandidateId} from 'utils/storage';
import { useDispatch, useSelector } from 'react-redux';
import { getoiComment } from 'store/DashboardPage/MyServices/actions';
import {InputField, TextArea} from 'formHandler/desktopFormHandler/formFields';
import CoursesServicesForm from 'formHandler/desktopFormHandler/formData/coursesServices';

const AddCommentModal = (props) => {
    const { addOpen, id, data }  = props;
    const dispatch = useDispatch();
    const { register, handleSubmit, errors, reset } = useForm();

    const submitComment = (values) => {
        const new_values = {
          ...values,
          candidate_id: getCandidateId(),
          oi_pk: data.oi_id,
          type: "POST",
        };

        dispatch(getoiComment(new_values));
        reset();
    };

    return (
        <Collapse in={addOpen == id}>
            <div className="position-relative" id={`openComment`+id}>
                <div className="db-add-comments lightblue-bg border-bottom-gray">
                    <ul className="db-timeline-list">
                        {data && data.comment.length > 0 ?
                            data.comment.map((comm, idx) => {
                                return(
                                    <li key={idx}>
                                        <i className="db-timeline-list--dot"></i>
                                        <span>{comm.created} {comm.addedBy ?  '   |   By ' + comm.addedBy : ""} </span>
                                        <p className="db-timeline-list--text">{comm.message ? comm.message : ""}</p>
                                    </li>
                                )
                            })
                            : ""
                        }
                    </ul>
                </div>

                <form onSubmit={handleSubmit(submitComment)}>
                    <div className="db-add-comments disabled-before lightblue-bg" id="addComments">
                        <span className="btn-close" onClick={() => !addOpen}>&#x2715;</span>
                        <p className="font-weight-semi-bold"> Add comment </p>
                        <TextArea attributes={CoursesServicesForm.name} register={register} errors={!!errors ? errors[CoursesServicesForm.name.name] : ''} />
                        <button type="submit" className="btn btn-outline-primary mt-20 px-5">Submit</button>
                    </div>
                </form>
            </div>
        </Collapse>
    )
}

export default AddCommentModal