import React from 'react';
import UIBanner from '../../../Common/UIBanner/UIbanner';
import ShineServices from './ShineServices/shineServices';

const ImproveProfile = (props) => {
    return (
        <div>
            {/* <UIBanner /> */}
            <UIBanner {...props} />
            {/* <GuidanceRecommendations /> */}
            {/* <ShineServices /> */}
            <ShineServices /> 
            {/* <ShineServicesStatus /> */}
        </div>
    )
}

export default ImproveProfile;