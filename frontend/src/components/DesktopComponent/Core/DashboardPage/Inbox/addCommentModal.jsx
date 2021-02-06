import React from 'react';
import { Collapse } from 'react-bootstrap';
import { useForm } from "react-hook-form";
import { useDispatch, useSelector } from 'react-redux';
import { fetchOiComment } from 'store/DashboardPage/AddSubmitComment/actions';
import { TextArea} from 'formHandler/desktopFormHandler/formFields';
import CoursesServicesForm from 'formHandler/desktopFormHandler/formData/coursesServices';
import Loader from '../../../Common/Loader/loader';
import { Toast } from '../../../Common/Toast/toast';
import { updateServiceCommentCount } from 'store/DashboardPage/MyServices/actions/index';
import { updateCourseCommentCount } from 'store/DashboardPage/MyCourses/actions/index';

const AddCommentModal = (props) => {
    const { addOpen, id, data, addCommentDataFetch, type } = props;
    const dispatch = useDispatch();
    const { register, handleSubmit, errors, reset } = useForm();
    const { commentLoader } = useSelector(store => store.loader);

    const submitComment = async (values) => {
        const new_values = {
          ...values,
          oi_pk: data.oi_id,
          type: "POST",
        };

        let response = await new Promise((resolve, reject) => dispatch(fetchOiComment({ payload: new_values, resolve, reject })));

        if (response?.error) {
            Toast.fire({
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
        reset();
    };

    return (
        <> { commentLoader && <Loader />}
        
        <Collapse in={addOpen == id}>
                <div className="position-relative" id={`openComment` + id}>
                    {
                        data && data.comment.length > 0 ?
                            <div className="db-add-comments lightblue-bg border-bottom-gray">
                                <ul className="db-timeline-list">
                                    {data.comment.map((comm, idx) => {
                                        return (
                                            <li key={idx}>
                                                <i className="db-timeline-list--dot"></i>
                                                <span>{comm.created} {comm.addedBy ? ' | By ' + comm.addedBy : ""} </span>
                                                <p className="db-timeline-list--text">{comm.message ? comm.message : ""}</p>
                                            </li>
                                        )
                                    })
                                    }
                                </ul>
                            </div>
                            : ""
                    }
                    
                    <form onSubmit={handleSubmit(submitComment)}>
                        <div className="db-add-comments disabled-before lightblue-bg" id="addComments">
                            <span className="btn-close" onClick={() => addCommentDataFetch(false)}>&#x2715;</span>
                            <p className="font-weight-semi-bold"> Add comment </p>
                            <TextArea attributes={CoursesServicesForm.name} register={register} errors={!!errors ? errors[CoursesServicesForm.name.name] : ''} />
                            <button type="submit" className="btn btn-outline-primary px-5">Submit</button>
                        </div>
                    </form>
                </div>
            </Collapse>
        </>
    )
}

export default AddCommentModal;