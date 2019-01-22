let images = document.querySelectorAll('source, img');

function loadImage(image) {
	let newImg = image.src.replace(/-thumbnail/, '');
	if (newImg !== image.src) image.src = newImg;
}
if ('IntersectionObserver'in window) {

	function handler(entries, observer) {
		for (let image of entries) {
			if (image.intersectionRatio > 0) {
				loadImage(image.target);
				observer.unobserve(image.target);
			}
		}
	}
	let config = {
		root: null,
		rootMargin: '0px',
		threshold: 0.5
	};
	let observer = new IntersectionObserver(handler, config);
	images.forEach(img => observer.observe(img));

} else {
	images.forEach(img => loadImage(img));
}