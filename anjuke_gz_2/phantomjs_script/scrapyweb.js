#!/usr/local/phantomjs/bin/phantomjs

var system = require('system');
var args = system.args;
if (args.length >= 2){
        var url = args[1];
        var timeOut = 10000;
        if (args.length == 3){
                timeOut = Math.min(30000, Math.max(0, args[2]));
        }

        var page = require('webpage').create();
        page.settings.userAgent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.76 Safari/537.36';
        page.open(encodeURI(url),
                        function(status){
                                if (status != 'success'){
                                        console.log('Err, status=' + status);
                                        phantom.exit(1);
                                }
                                console.log(page.content);
                                phantom.exit();
                        });
        setTimeout(function(){
                console.log(page.content);
                phantom.exit();
        }, timeOut);}else {
        console.log('Usage:');
        console.log('\tphantomjs scrapyweb.js url timeout');
        phantom.exit(1);}
