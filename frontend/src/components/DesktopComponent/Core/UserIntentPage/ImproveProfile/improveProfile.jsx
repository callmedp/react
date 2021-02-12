import React, { useRef, useEffect } from 'react';
import UIBanner from './UIBanner/UIbanner';
import UIBanner1 from './UIBanner/UIbanner1';
import GuidanceRecommendations from '../FindRightJob/GuidanceRecommendations/guidanceRecommendations';
import ShineServices from './ShineServices/shineServices';
import ShineServicesStatus from './ShineServices/shineServicesStatus'

const ImproveProfile = (props) => {
    return (
        <div>
            {/* <UIBanner /> */}
            <UIBanner1 />
            {/* <GuidanceRecommendations /> */}
            {/* <ShineServices /> */}
            <ShineServicesStatus />
        </div>
    )
}

export default ImproveProfile;