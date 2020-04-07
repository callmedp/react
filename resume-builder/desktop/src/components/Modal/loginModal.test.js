import { shallow } from 'enzyme';
import React from 'react';
import LoginModal from './loginModal';


describe('LoginModalTest', () => {

    it('Login Modal debug', () => {
        const  props ={
            ui: {
                loginModal: true
            }
        },
         ModalWrapperComponent = shallow(<LoginModal {...props} />);
        expect(ModalWrapperComponent).toMatchSnapshot();
    });
})

