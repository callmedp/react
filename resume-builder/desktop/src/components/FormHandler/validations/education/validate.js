const validate = values => {
    const errors = {};
    const listErrors = []
    values = (values && values.list) || [];
    values.forEach((obj, objIndex) => {
        const objErrors = {}
        objErrors.institution_name = !obj || !obj.institution_name ? 'Required' : undefined;
        objErrors.degree = !obj || !obj.degree ? 'Required' : undefined;
        objErrors.specialization = !obj || !obj.specialization ? 'Required' : undefined;
        objErrors.start_date = !obj || !obj.start_date ? 'Required' : undefined;
        objErrors.end_date = !obj || (!obj.end_date && !obj.is_pursuing) ? 'Required' : undefined;
        objErrors.course_type = !obj || !obj.course_type ? 'Required' : undefined;
        objErrors.percentage_cgpa = obj && obj.percentage_cgpa && isNaN(Number(obj.percentage_cgpa)) ? 'Must be a number' : obj.percentage_cgpa >100 ? 'Must be less than 100': undefined
        listErrors[objIndex] = objErrors
    });
    if (listErrors.length) {
        errors.list = listErrors;
        return errors;

    }

    return errors;

};


export default validate;