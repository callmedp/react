import React from 'react';

import GuidanceRecommendations from './Guidance/guidanceRecommendations';
import Footer from '../../../Common/Footer/Footer';

const UserGuidance = (props) => {
    return (
        <div>
            <GuidanceRecommendations />
            <Footer pageType={'user_intent_user_guidance'} />
        </div>
    )
}

export default UserGuidance;