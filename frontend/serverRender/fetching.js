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
    console.error('Error occured in fetching Apis ');
    console.log("window configurations :",window?.config)
    console.log("Make sure api hits are going to the correct domain. If not run pm2 again with proper configuration.")
    reject(error)
  }
  return resolve(results);
}

export default fetchApiData;