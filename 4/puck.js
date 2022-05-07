const { execSync } = require('child_process');

let output
output = execSync('cd puckLetter;sudo node a.js;sudo node b.js', {encoding: 'utf-8'});