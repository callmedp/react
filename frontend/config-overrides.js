const path = require('path');
const fs = require('fs');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

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
const appBuild = resolveApp('ssrBuild');
const publicUrl = '/';
const indexHtml = '../../../frontend/ssrBuild/index.html';
const indexMobileHtml = '../../../frontend/ssrBuild/index.mobile.html';
const appHtml = resolveApp('public/index.html');

module.exports = {
  webpack: function (config, env) {
    config.entry = {
      desktop: appDesktopIndexJs,
      mobile: appMobileIndexJs
    };

    // config.output = {
    //   ...config.output,
    //   filename : 
    // }
    config.module.rules[2].oneOf[5].use[4].options.prependData = '$image-path: ' + JSON.stringify(process.env.REACT_APP_IMAGE_URL) + ';';
    

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
    config.plugins[0].options.filename = indexHtml

    config.plugins.push(new HtmlWebpackPlugin(
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
    ))

    // config.resolve = {
    //   ...config.resolve,
    //   alias: { 'media': '/media/static/react/media' },
    // };

    // config.plugins.push(new BundleAnalyzerPlugin());

  
    return config;
  },

  paths: function (paths, env) {

    paths.appBuild = appBuild;
    paths.publicUrlOrPath = publicUrl;

    return paths;
  }
}