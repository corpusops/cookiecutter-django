const path = require('path');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const { WebpackManifestPlugin } = require('webpack-manifest-plugin');
const VueLoaderPlugin = require('vue-loader/lib/plugin')
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
    mode: 'development',
    entry: {
        app: './frontend/app.js',
        style: './frontend/scss/style.scss',
    },
    optimization: {
        splitChunks: {
            chunks: 'all',
            cacheGroups: {
                style: {
                    name: 'style',
                    type: 'css/mini-extract',
                    chunks: 'all',
                    enforce: true,
                },
            },
        },
    },
    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: 'vue-loader',
            },
            {
                test: /style\.scss$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    'css-loader',
                    'sass-loader',
                ],
            },
            {
                test: /\.css$/,
                use: [
                    'vue-style-loader',
                    'style-loader',
                    'css-loader',
                ],
            },
            {
                test: /\.(png|svg|jpe?g|gif|woff2?|ttf|eot)$/,
                use: ['url-loader'],
            },
        ],
    },
    devServer: {
        hot: true,
        devMiddleware: {writeToDisk: true},
        client: { logging: 'info'},
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, PATCH, OPTIONS',
            'Access-Control-Allow-Headers': 'X-Requested-With, content-type, Authorization',
        },
    },
    plugins: [
        new VueLoaderPlugin(),
        new MiniCssExtractPlugin({
            filename: '[name].[contenthash].css',
        }),
        new CleanWebpackPlugin({ protectWebpackAssets: false }),
        new WebpackManifestPlugin({
            publicPath: 'dist/',
            generate: (seed, files) => {
                const entrypoints = new Set()
                files.forEach(
                  (file) => ((file.chunk || {})._groups || []).forEach(
                    (group) => entrypoints.add(group),
                  ),
                )
                const entries = [...entrypoints]
                return entries.reduce((acc, entry) => {
                    const name = (entry.options || {}).name
                      || (entry.runtimeChunk || {}).name
                    const files = [].concat(
                      ...(entry.chunks || []).map((chunk) => [...chunk.files]),
                    ).filter(Boolean).map(f => 'dist/' + f)
                    return name ? { ...acc, [name]: files } : acc
                }, seed)
            },
        }),
    ],
    output: {
        publicPath: '/static/dist/',
        filename: '[name].[contenthash].js',
        path: path.resolve(__dirname, 'src/{{cookiecutter.django_project_name}}/static/dist'),
    },
};
