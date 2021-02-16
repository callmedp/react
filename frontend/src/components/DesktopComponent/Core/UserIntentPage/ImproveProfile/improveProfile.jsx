import React, { useRef, useEffect } from 'react';
import UIBanner from '../../../Common/UIBanner/UIbanner';
import UserGuidance from '../UserGuidance/UserGuidance';
import ShineServices from './ShineServices/shineServices';
import ShineServicesStatus from './ShineServices/shineServicesStatus'

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