import { shallow } from 'enzyme';
import React from 'react';
import HelpModal from './helpModal';


describe('HelpModalTest', () => {

    it('Help Modal debug', () => {
        const ModalWrapperComponent = shallow(<HelpModal  />);
        expect(ModalWrapperComponent).toMatchSnapshot();
    });
})

