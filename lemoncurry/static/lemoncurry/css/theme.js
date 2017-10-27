const {join} = require('path');
const {readFileSync} = require('fs');

const stylus = require('stylus');
const {safeLoad} = require('js-yaml');

const themePath = join(__dirname, '..', '..', 'base16-materialtheme-scheme', 'material-darker.yaml');

module.exports = function() {
	const theme = safeLoad(readFileSync(themePath, 'utf8'));
	return function(style) {
		for (let i = 0; i < 16; i++) {
			const key = 'base0' + i.toString(16).toUpperCase();

			style.define('$' + key, new stylus.nodes.Literal('#' + theme[key]));
		}
	};
};
