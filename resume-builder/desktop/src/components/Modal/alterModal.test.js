import { shallow} from 'enzyme';
import React from 'react';
import AlertModal  from './alertModal';


describe('AlertModal', () => {

    it('Alert modal  debug case ', () => {  
        const props = {
            ui: {
                alertModal : true,
                generateResumeModal: false
            },
            nextLink: null,
            newUser: false,
            isPreview: false
        },
         ModalWrapperComponent = shallow(<AlertModal {...props} />);
        expect(ModalWrapperComponent).toMatchSnapshot();
    });
})

