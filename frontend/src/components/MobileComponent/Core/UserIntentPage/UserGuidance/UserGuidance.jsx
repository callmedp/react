import React, { useRef, useEffect } from 'react';
// import UIBanner from '../../../Common/UIBanner/UIbanner';
import GuidanceRecommendations from './Guidance/guidanceRecommendations';

const UserGuidance = (props) => {
    return (
        <div>
            {/* <UIBanner {...props} /> */}
            <GuidanceRecommendations />
        </div>
    )
}

export default UserGuidance;