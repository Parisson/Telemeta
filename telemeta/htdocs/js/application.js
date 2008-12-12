function ployBlocks() {
 
  $('.extraInfos div.nett').css('display', 'block');
  $('.closed').css('display', 'none');
	$('.extraInfos h4').toggleClass('on').click(function() {
      $(this)
          .toggleClass('on')
          .parent().find('div').eq(0).toggle();
      return false;
  });

  /*
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
  */
}
