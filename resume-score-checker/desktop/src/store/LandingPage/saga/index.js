




import { Api } from './Api';


function* fetchFileUrl(action) {
    try {
        const { payload: { uploadFile, resolve } } = action;

        var data = new FormData();

        data.append('file',file)

        const result = yield call(Api.fetchImageUrl, data, candidateId);

        yield put({ type: UPDATE_UI, data: { loader: false } })

        return resolve(result['data']['path'])


    } catch (e) {

        console.log('error', e);
    }
}


