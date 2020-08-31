import { shallow } from 'enzyme';
import React from 'react';
import MenuModal from './menuModal';


describe('MenuModal', () => {

    it('Menu Modal debug', () => {
        const  props ={
            preferenceList :[]
        },
         ModalWrapperComponent = shallow(<MenuModal {...props} />);
        expect(ModalWrapperComponent).toMatchSnapshot();
    });
})

