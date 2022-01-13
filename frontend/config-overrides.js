const path = require('path');
const fs = require('fs');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const WorkboxWebpackPlugin = require('workbox-webpack-plugin');

const appDirectory = fs.realpathSync(process.cwd());
const resolveApp = relativePath => path.resolve(appDirectory, relativePath);


const moduleFileExtensions = [
  'web.mjs',
  'mjs',
  'web.js',
  'js',
  'web.ts',
  'ts',
  'web.tsx',
  'tsx',
  'json',
  'web.jsx',
  'jsx',
];

const resolveModule = (resolveFn, filePath) => {
  const extension = moduleFileExtensions.find(extension =>
    fs.existsSync(resolveFn(`${filePath}.${extension}`))
  );

  if (extension) {
    return resolveFn(`${filePath}.${extension}`);
  }

  return resolveFn(`${filePath}.js`);
};

const appDesktopIndexJs = resolveModule(resolveApp, 'src/index.desktop');
const appMobileIndexJs = resolveModule(resolveApp, 'src/index.mobile');
const swSrc = resolveModule(resolveApp, 'src/service-worker');

const appHtml = '!!raw-loader!public/serverIndex.ejs';
const appBuild = resolveApp('./build');
const indexHtml = '../views/index.ejs';
const indexMobileHtml = '../views/indexMobile.ejs';

module.exports = {
  webpack: function (config, env) {
    config.entry = {
      desktop: appDesktopIndexJs,
      mobile: appMobileIndexJs
    };
    

    config.plugins[6].opts.generate = (seed, files, entrypoints) => {
      const manifestFiles = files.reduce((manifest, file) => {
        manifest[file.name] = file.path;
        return manifest;
      }, seed);
      const entrypointFiles = entrypoints.desktop.filter(
        fileName => !fileName.endsWith('.map')).
        concat(entrypoints.mobile.filter(
          fileName => !fileName.endsWith('.map')
        ))

      return {
        files: manifestFiles,
        entrypoints: entrypointFiles,
      };
    };

    config.plugins[0].options.excludeChunks = ['mobile']
    config.plugins[0].options.filename = indexHtml;
    config.plugins[0].options.template = appHtml;

    config.plugins[8] = new HtmlWebpackPlugin(
      Object.assign(
        {},
        {
          inject: true,
          template: appHtml,
          filename: indexMobileHtml,
          excludeChunks: ['desktop']
        },
        {
          minify: {
            removeComments: true,
            collapseWhitespace: true,
            removeRedundantAttributes: true,
            useShortDoctype: true,
            removeEmptyAttributes: true,
            removeStyleLinkTypeAttributes: true,
            keepClosingSlash: true,
            minifyJS: true,
            minifyCSS: true,
            minifyURLs: true,
          },
        }
      )
    )
    
    fs.existsSync(swSrc) && config.plugins.push(
    new WorkboxWebpackPlugin.InjectManifest({
      swSrc,
      exclude: [/\.map$/, /asset-manifest\.json$/, /LICENSE/],
    }))


  
    return config;
  },

  paths: function (paths, env) {

    paths.appBuild = appBuild;

    return paths;
  }
}