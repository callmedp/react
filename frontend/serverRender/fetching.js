const fetchApiData = async ({ dispatch }, params, actionGroup, resolve, reject) => {

  let actionList = actionGroup(params);
  let results = [];

  try {

    results = await Promise.all((actionList || []).map((caller, index) => {
      return new Promise((resolve, reject) =>
        dispatch(caller['action']({ ...caller.payload, resolve, reject })))
    })
    )
  }
  catch (error) {
    console.log('Error occured in skillPageApi ', error);
    reject(error)
  }
  return resolve(results);
}

export default fetchApiData;