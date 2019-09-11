let shell = require('shelljs');


/* Set timestamp  */
const currentTimeStamp = +new Date();

shell.echo(`${shell.pwd()}`);

/* delete the files currently available */
shell.exec('rm -rf ../careerplus/static_core/react/dist/desktop/*');

shell.exec('rm -rf ../careerplus/static_core/react/dist/mobile/*');

shell.echo('Removed file <><><><><><> ');

/*create client react js build using  same timestamp*/

shell.exec(`node desktop/scripts/build-non-split.js ${currentTimeStamp}`);


shell.echo('<><><><><><>< Created desktop build ><><><><><><>');

shell.exec(`node mobile/scripts/build-config.js ${currentTimeStamp}`);

shell.echo('<><><><><><>< Created mobile build ><><><><><><>');

/*create server build */

shell.exec(`webpack --config  ./server/webpack.server.config.js`);


shell.echo('<><><><><><>< created server build ><><><><><>');

/*remove build first*/
//
// if (shell.find('./scripts/server.js').length) {
//
//     shell.exec('rm  ./scripts/server.js')
// }

// shell.echo('<><><><><><>< removed previous server build ><><><><><>');

/*execute build */

shell.exec(` node ./server/server.js  ${currentTimeStamp}`);


shell.echo('<><><><><><>< executed server build ><><><><><>');


