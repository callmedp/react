const validate = values => {
  const errors = {};
  if (!values.list || !values.list.length) {
      errors.list = {_error: 'Atleast One Language should be entered.'}
      return errors;
  }
  const listErrors = []
  values.list.forEach((obj, objIndex) => {
      const objErrors = {}
      objErrors.name = !obj || !obj.name ? 'Required' : undefined;
      objErrors.proficiency = !obj || !obj.proficiency ? 'Required' : undefined;
      listErrors[objIndex] = objErrors
  });
  if (listErrors.length) {
      errors.list = listErrors;
      return errors;
  }
}

export default validate;