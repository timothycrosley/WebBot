#!/bin/sh

compass compile
cat js/py-builtins.js js/WebElements.js js/DynamicForm.js > js/WebBot.js
