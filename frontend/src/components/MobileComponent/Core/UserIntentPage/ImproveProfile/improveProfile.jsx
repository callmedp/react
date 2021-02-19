import React, { useRef, useEffect } from 'react';
import GuidanceRecommendations from '../UserGuidance/Guidance/guidanceRecommendations';
import ShineServices from './ShineServices/shineServices';
import ShineServicesStatus from './ShineServices/shineServicesStatus';
import UploadModal from '../../../Common/Modals/uploadModal';


const ImproveProfile = (props) => {
    return (
        <div>
            {/* <GuidanceRecommendations /> */}
            <ShineServices />
            {/* <ShineServicesStatus /> */}
            {/* <UploadModal /> */}
        </div>
    )
}

export default ImproveProfile;