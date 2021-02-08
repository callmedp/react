import React, {useEffect} from 'react';
import { Collapse } from 'react-bootstrap';
import { useDispatch, useSelector } from 'react-redux';
import { fetchOiDetails } from 'store/DashboardPage/MyServices/actions/index';
import Loader from '../../../Common/Loader/loader';
import { startOiDetailsLoader, stopOiDetailsLoader } from 'store/Loader/actions/index';

const ViewDetailModal = (props) => {
    const { id, toggleDetails, isOpen } = props;
    const dispatch = useDispatch()
    const { oiDetailsLoader } = useSelector(store => store.loader);
    const oiDetailsData = useSelector(store => store.oiDetails?.data);

    const handleEffects = async () => {
        try{
            dispatch(startOiDetailsLoader());
            await new Promise((resolve, reject) => dispatch(fetchOiDetails({payload: id, resolve, reject})));
            dispatch(stopOiDetailsLoader());
        }
        catch(e){
            dispatch(stopOiDetailsLoader());
        }
    };

    useEffect(() => {
        handleEffects()
    }, [id])

    return (
        <>
            {
                oiDetailsLoader && <Loader />
            }
            <Collapse in={isOpen == id}>
            <div className="db-view-detail arrow-box left-big" id={`openViewDetail`+id}>
            <span className="btn-close" onClick={() => toggleDetails(id)}>&#x2715;</span>
                <ul className="db-timeline-list">
                    { 
                        oiDetailsData?.map((det, ind) => {
                            return (
                                <li key={ind}>
                                    <i className="db-timeline-list--dot"></i>
                                    <span>{det.date}</span>
                                    <p className="db-timeline-list--text">{det.status}</p>
                                </li>
                            )
                        })
                
                    }
                </ul>
            </div>
        </Collapse>
    </>
    )
}

export default ViewDetailModal;