

var HtmlWebpackPlugin = require('html-webpack-plugin');
var path = require('path');
var webpack = require('webpack');

module.exports = function(grunt) {

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        concat: {
            css: {
                src: ['public/scss/*'],
                dest: 'temp_scss.scss' 
            } 
        }, 

        webpack: {
            app: {
                module: {
                    loaders: [
                        {
                            test: /\.scss$/,
                            loader: 'style!css!sass'
                        }, 
                        {
                            test: /\.hbs$/,
                            loader: 'handlebars-loader'
                        },
                        {
                            test: /\.js$/, 
                            loader: 'jsx-loader'
                        }
                    ] 
                }, 

                entry: './public/main.js',

                output: {
                    path: path.join(__dirname, 'build/js/'),
                    filename: 'bundle.[hash].js',
                    publicPath: '/js/' 
                },

                stats: {
                    colors: false,
                    modules: false,
                    reasons: false
                },

                storeStatsTo: 'bundle_hash',
                plugins: [
                    new HtmlWebpackPlugin({
                        title: 'webpack pres',
                        filename: '../index.html',
                        template: './views/index.html' 
                    })  
                ]
            } 
        },

        sass: {
            dist: {
                options: {
                    style: 'compressed' 
                }, 
                files: {
                    'build/css/style.<%= bundle_hash.hash %>.css': 'temp_scss.scss' 
                }
            }
        },

        clean: {
            bundles: ['build/js/**/*', '!build/js/bundle.<%= bundle_hash.hash %>.js', '!build/js/*.bundle.<%= bundle_hash.hash %>.js', 'build/css/**/*', 'temp_scss.scss', '!build/css/style.<%= bundle_hash.hash %>.css']
        },

        watch: {
            scripts: {
                files: ['public/**/*', 'views/index.html'],
                tasks: ['concat', 'webpack', 'sass', 'clean']  
            } 
        }
        
    });

    require('load-grunt-tasks')(grunt);

    grunt.registerTask('default', ['concat', 'webpack', 'sass', 'clean']);
    
    grunt.event.on('watch', function(action, filepath, target) {
        grunt.log.writeln(target + ': ' + filepath + ' has ' + action);
    });

};
