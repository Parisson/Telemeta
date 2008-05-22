function ployBlocks() {
	var extraInfos = $$('.extraInfos div');
	for (i = 0; i <extraInfos.length; i++ ) {
		if(!extraInfos[i].hasClassName('nett')) {
			extraInfos[i].style.display = 'block';
		}
	}
	var blocks = $$('.closed');
	for (i = 0; i <blocks.length; i++ ) {
		blocks[i].style.display = 'none';
	}
	var extraInfos = $$('.extraInfos h4');
	for (i = 0; i <extraInfos.length; i++ ) {
		extraInfos[i].toggleClassName('on');
		extraInfos[i].onclick = function() {
			this.parentNode.getElementsByTagName("div")[0].toggle();
			this.toggleClassName('on');
			return false;
		}
	}
}