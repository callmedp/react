let shell = require('shelljs');


/* Set timestamp  */
const currentTimeStamp = +new Date();

/* delete the files currently available */
shell.exec('rm -rf ../../careerplus/static_core/react/dist/desktop/*')

shell.echo('Removed file <><><><><><>');

/*create client react js build using  same timestamp*/

shell.exec(`node ./scripts/build-non-split.js ${currentTimeStamp}`);

shell.echo('<><><><><><>< Created script ><><><><><><>');

/*create server build */

shell.exec(`webpack --config  ./scripts/webpack.server.config.js`);


shell.echo('<><><><><><>< created server build ><><><><><>');

/*remove build first*/
//
// if (shell.find('./scripts/server.js').length) {
//
//     shell.exec('rm  ./scripts/server.js')
// }

// shell.echo('<><><><><><>< removed previous server build ><><><><><>');

/*execute build */

shell.exec(` node ./scripts/server.js  ${currentTimeStamp}`);


shell.echo('<><><><><><>< executed server build ><><><><><>');


