import { shallow } from 'enzyme';
import React from 'react';
import SelectTemplateModal from './selectTemplateModal';


describe('SelectTemplateModal', () => {

    it('Select Template Modal debug', () => {
        const  props ={
            ui: {
                'select_template_modal': true 
            }
        },
         ModalWrapperComponent = shallow(<SelectTemplateModal {...props} />);
        expect(ModalWrapperComponent).toMatchSnapshot();
    });
})

