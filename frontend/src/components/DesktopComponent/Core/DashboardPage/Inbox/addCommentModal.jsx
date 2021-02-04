import React from 'react';
import { Collapse } from 'react-bootstrap';
import { useForm } from "react-hook-form";
import { useDispatch, useSelector } from 'react-redux';
import { fetchOiComment } from 'store/DashboardPage/AddSubmitComment/actions';
import { TextArea} from 'formHandler/desktopFormHandler/formFields';
import CoursesServicesForm from 'formHandler/desktopFormHandler/formData/coursesServices';
import Loader from '../../../Common/Loader/loader';

const AddCommentModal = (props) => {
    const { addOpen, id, data, setAddOpen }  = props;
    const dispatch = useDispatch();
    const { register, handleSubmit, errors, reset } = useForm();
    const { commentLoader } = useSelector(store => store.loader);

    const submitComment = async (values) => {
        const new_values = {
          ...values,
          oi_pk: data.oi_id,
          type: "POST",
        };

        await new Promise((resolve, reject) => dispatch(fetchOiComment({payload: new_values, resolve, reject})));
        reset();
    };

    return (
        <> { commentLoader && <Loader />}
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
                        <span className="btn-close" onClick={() => setAddOpen(state => !state)}>&#x2715;</span>
                        <p className="font-weight-semi-bold"> Add comment </p>
                        <TextArea attributes={CoursesServicesForm.name} register={register} errors={!!errors ? errors[CoursesServicesForm.name.name] : ''} />
                        <button type="submit" className="btn btn-outline-primary mt-20 px-5">Submit</button>
                    </div>
                </form>
            </div>
        </Collapse>
        </>
    )
}

export default AddCommentModal;