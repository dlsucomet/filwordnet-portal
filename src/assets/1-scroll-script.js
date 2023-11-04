function get_position(id) {
	const yOffset = -1.2 * document.getElementById('search-word-div').clientHeight;
	return document.getElementById(id).getBoundingClientRect().top + window.pageYOffset + yOffset;
}

function make_bold(id) {
	const links = ['senses-link', 'plot-sense-link', 'plot-source-link', 'embeddings-link', 'network-link', 'export-link'];
	for (let link of links) {
		if (link != id) {
			document.getElementById(link).classList.remove('bold');
		} else {
			document.getElementById(link).classList.add('bold');
		}
	}
}

window.addEventListener('scroll', function (e) {
	const SCROLL_THRESHOLD = 100;
	const displacement = window.pageYOffset !== undefined ? window.pageYOffset : (document.documentElement || document.body.parentNode || document.body).scrollTop;

	if (window.innerHeight + window.pageYOffset >= document.body.offsetHeight - 2) {
		make_bold('export-link');
	} else if (Math.abs(displacement - get_position('network-row')) < SCROLL_THRESHOLD) {
		make_bold('network-link');
	} else if (Math.abs(displacement - get_position('plot-sense-row')) < SCROLL_THRESHOLD) {
		make_bold('plot-sense-link');
	} else if (Math.abs(displacement - get_position('plot-source-row')) < SCROLL_THRESHOLD) {
		make_bold('plot-source-link');
	} else if (Math.abs(displacement - get_position('embeddings-row')) < SCROLL_THRESHOLD) {
		make_bold('embeddings-link');
	} else if (displacement < get_position('plot-sense-row')) {
		make_bold('senses-link');
	}
});
