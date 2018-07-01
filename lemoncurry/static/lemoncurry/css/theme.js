const {join} = require('path');
const {readFileSync} = require('fs');

const stylus = require('stylus');
const {safeLoad} = require('js-yaml');

const themePath = join(__dirname, '..', '..', 'base16-materialtheme-scheme', 'material-darker.yaml');

const breakpoints = {
	sm: 576,
	md: 768,
	lg: 992,
	xl: 1200,
};

module.exports = function() {
	const theme = safeLoad(readFileSync(themePath, 'utf8'));
	return function(style) {
		for (let key in breakpoints) {
			style.define('$' + key, new stylus.nodes.Unit(breakpoints[key], 'px'));
		}

		for (let i = 0; i < 16; i++) {
			const key = 'base0' + i.toString(16).toUpperCase();
			const hex = theme[key];
			const colour = new stylus.nodes.RGBA(
				parseInt(hex.substr(0, 2), 16),
				parseInt(hex.substr(2, 2), 16),
				parseInt(hex.substr(4, 2), 16),
				1
			);

			style.define('$' + key, colour);
		}
	};
};
