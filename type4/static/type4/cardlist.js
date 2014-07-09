function init_cardlist() {
			
	function getCardUrl(cardname) {
		return 'http://magiccards.info/query?q=' + cardname;
	}
	
	function getImage(cardname) {
		return '<img class="cardimage" src="http://mtgimage.com/card/'
			+ cardname
			+ '.jpg"><img/>';
	}

	function getCardDiv(showArt, cardname) {
		if(showArt) {
			return '<a href="'
				+ getCardUrl(cardname)
				+ '">'
				+ getImage(cardname)
				+ '</a>';
		} else {		
			return '<li><a href="'
				+ getCardUrl(cardname)
				+ '">'
				+ cardname
				+ '</a></li>';
		}
	}

	function toggle(elm){
		var $this = elm;
		$this.find('.cardlistdisplay').remove();
		
		var cardnames = $this.find('.data').html().split('|');
		var showArt = $this.data('art');
		$this.data('art', !showArt);
	
		var html = '';
		for (i = 0; i < cardnames.length; i++) {
			var name = cardnames[i].trim();
			html += getCardDiv(showArt, name);
		}
		if (showArt) {
			html = '<div class="cardlistdisplay">'
				+ html 
				+ '</div>';
		} else {
			html = '<div class="cardlistdisplay"><ul>'
				+ html
				+ '</ul></div>';
		}		
		$this.append(html);
	}

	$('.cardlist').each(function () {
		var $this = $(this);
		$this.find('.toggle').click(function (){
			toggle($this);
		});
		toggle($this); //run now for init
	});
}