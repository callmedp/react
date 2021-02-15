import React, { useRef, useEffect } from 'react';
import UIBanner from '../../../Common/UIBanner/UIbanner';
import FindJob from './FindJob/findJob';

const FindRightJob = (props) => {
    
    return (
        <div>
            <UIBanner {...props} />
            <FindJob />
        </div>
    )
}

export default FindRightJob;