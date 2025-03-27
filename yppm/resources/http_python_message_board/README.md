# A simple pure python http project
It only uses python,html,css,es5 javascript code.

It supports python2.7, python3.2, python3.10 and all 2014 year old browser.

## How to use it?
Just use 'python3.2 main.py'

Then visit http://localhost:8899

## How to sync to server
rsync -avz --progress --delete ./ root@87.50:/root/yppm/yppm/resources/http_python_message_board/

## Problem
* Found cloudflare will ignore all post data from html form, so the server gets nothing to save.
