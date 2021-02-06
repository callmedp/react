import React from 'react';
import Swal from 'sweetalert2';
import { useDispatch, useSelector } from 'react-redux';
import { CandidateAcceptRejectResume } from 'store/DashboardPage/MyServices/actions/index';
import { startAcceptRejectLoader, stopAcceptRejectLoader } from 'store/Loader/actions/index';
import Loader from '../../../Common/Loader/loader';
import { fetchMyServices } from 'store/DashboardPage/MyServices/actions';

const AcceptModal = (props) => {
    const { setAcceptModal, oi_id, currentPage } = props

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
                await new Promise((resolve, reject) => dispatch(fetchMyServices({page: currentPage, resolve, reject })));
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
                    <p className="font-weight-bold fs-16 mt-20 mb-0">Are you sure you want to accept?</p>
                    <p>Once you accept, your service will be closed.</p>
                    <div className="m-form-group mt-15">
                        <button className="btn btn-blue px-30" onClick={() => acceptRejectHandler("accept", oi_id)}>Accept</button>&emsp;
                    </div>
                </div>
            </div>
        </>
    )
}

export default AcceptModal;