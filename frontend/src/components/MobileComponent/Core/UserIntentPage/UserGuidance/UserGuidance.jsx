import React, { useRef, useEffect } from 'react';

import GuidanceRecommendations from './Guidance/guidanceRecommendations';
import Footer from '../../../Common/Footer/Footer';

const UserGuidance = (props) => {
    return (
        <div>
            <GuidanceRecommendations />
            <Footer />
        </div>
    )
}

export default UserGuidance;