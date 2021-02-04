import React from 'react';
import Swal from 'sweetalert2';
import { useDispatch, useSelector } from 'react-redux';
import { CandidateAcceptRejectResume } from 'store/DashboardPage/MyServices/actions/index';
import { startAcceptRejectLoader, stopAcceptRejectLoader } from 'store/Loader/actions/index';
import Loader from '../../../Common/Loader/loader';

const AcceptModal = (props) => {
    const { setAcceptModal, oi_id } = props

    const dispatch = useDispatch()
    const { acceptRejectLoader } = useSelector(store => store.loader);

    const acceptRejectHandler = async (type, id) => {
        if (type === "accept") {
            let acceptValues = {
                oi_pk: id,
                type
            }
          try {
                dispatch(startAcceptRejectLoader());
                await new Promise((resolve, reject) => { dispatch(CandidateAcceptRejectResume({ payload: acceptValues, resolve, reject })); });
                dispatch(stopAcceptRejectLoader());

                setAcceptModal(false)
                Swal.fire({
                icon: 'success',
                title: 'Accept Request Sent!'
                })
            } catch (e) {
                dispatch(stopAcceptRejectLoader());
                Swal.fire({
                icon: "error",
                title: "Something went wrong! Try Again",
                });
            }
        }
    };

    return (
        <>
            { acceptRejectLoader && <Loader /> }
            <div className="m-slide-modal">
                <span className="m-db-close" onClick={() => setAcceptModal(false)}>&#x2715;</span>
                <div className="text-center">
                    <strong>Are you sure you want to accept?</strong><br />
                    <span className="d-block mt-15">Note: Once you accept, your service will be closed.</span>
                    <br/><br/>
                    <div className="m-form-group">
                        <button className="btn btn-blue px-30" onClick={() => acceptRejectHandler("accept", oi_id)}>Accept</button>&emsp;
                    </div>
                </div>
            </div>
        </>
    )
}

export default AcceptModal;