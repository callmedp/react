import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchOiDetails } from 'store/DashboardPage/MyServices/actions/index';
import Loader from '../../../Common/Loader/loader';
import { startOiDetailsLoader, stopOiDetailsLoader } from 'store/Loader/actions/index';

const ViewDetails = (props) => {
    const { id } = props
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
            <ul className="my-order__order-detail--info mt-15">
                {
                    oiDetailsData?.map((data, index) =>
                        <li key={index}>
                            <span> 
                                {/* <hr /> */}
                                {data?.date} <br />
                                <strong> {data?.status} </strong>
                            </span>
                        </li>)
                }
            </ul>
        </>
    )
}

export default ViewDetails;