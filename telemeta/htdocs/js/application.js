function ployBlocks() {
	var blocks = $$('.extraInfos div');
	for (i = 0; i <blocks.length; i++ ) {
		if(!blocks[i].hasClassName('nett')) {
			blocks[i].style.display = 'none';
		}
	}
	var extraInfos = $$('.extraInfos h4');
	for (i = 0; i <extraInfos.length; i++ ) {
		extraInfos[i].toggleClassName('on');
		extraInfos[i].onclick = function() {
			this.parentNode.getElementsByTagName("div")[0].toggle();
			this.toggleClassName('on');
		}
	}
}