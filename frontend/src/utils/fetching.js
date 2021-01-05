const fetchApiData = async ({ dispatch }, params, actionGroup) => {

    let actionList = actionGroup(params);
  
    let results = [];
    try {
     
      results = await Promise.all(
        (actionList || []).map((caller,index) => {
         
          return new Promise((resolve, reject) =>
            dispatch(caller['action']({
              ...caller.payload,
              resolve,
              reject
            })))
        })
      )
    }
    catch (e) {
      console.log('Error occured in skillPageApi ', e);
      
    }
    return results;
  }
  
  export default fetchApiData;