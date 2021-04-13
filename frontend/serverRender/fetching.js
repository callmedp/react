const fetchApiData = async ({ dispatch }, params, cookies, actionGroup, resolve, reject) => {
  let actionList = actionGroup(params);
  let results = [];
  
  try {
    results = await Promise.all((actionList || []).map((caller, index) => {
    let data = { ...caller.payload, em: cookies };
      return new Promise((resolve, reject) => {
        console.log('3>>>>>>>>>>>', hello)
        
        const hello = dispatch(caller['action']({ payload: { ...data}, resolve, reject }))});
      })
    )
  }
  catch (error) {
    console.log('4>>>>>>>>>>>', error)

    console.error('Error occured in fetching Apis ');
    console.log("window configurations :", window?.config)
    console.log("Make sure api hits are going to the correct domain. If not run pm2 again with proper configuration.")
    reject(error)
  }
  return resolve(results);
}

export default fetchApiData;