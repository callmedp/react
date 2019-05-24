const validate = values => {
    const errors = {};
    if (!values.list || !values.list.length) {
        errors.list = {_error: 'Atleast One Education should be entered.'}
        return errors;
    }
    else{
        const listErrors = []
        values.list.forEach((obj, objIndex) => {
            const objErrors = {}
            objErrors.institution_name = !obj || !obj.institution_name ? 'Required' : undefined;
            objErrors.specialization = !obj || !obj.specialization ? 'Required' : undefined;
            objErrors.start_date = !obj || !obj.start_date ? 'Required' : undefined;
            objErrors.end_date = !obj || (!obj.end_date && !obj.is_pursuing) ? 'Required' : undefined;
            objErrors.course_type = !obj || !obj.course_type ? 'Required' : undefined;
            listErrors[objIndex] = objErrors
        });
        if (listErrors.length) {
            errors.list = listErrors;
            ////console.log(errors)
            return errors;
        }
    }
    
};


export default validate;