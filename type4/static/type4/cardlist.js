function init_cardlist() {
	
	function getCardUrl(cardname) {
		return 'http://magiccards.info/query?q=' + cardname;
	}
	
	function getImage(cardname) {
		return '<img src="http://mtgimage.com/card/' + cardname + '.jpg" width="300"><img/>';
	}

	function getCardDiv(cardname) {
		return '<a href="'
			+ getCardUrl(cardname)
			+ '">'
			+ getImage(cardname)
			+ '</a>';
	}

	function makeInnerDiv(cardnames){
		var html = '';
		for (i = 0; i < cardnames.length; i++) {
			var name = cardnames[i].trim();
			console.log(name);
			html += getCardDiv(name);
		}
		return '<div class="cardlistdisplay">'
			+ html + '</div>';
	}

	function run(){
		$('.cardlistdisplay').remove();
		var cardlists = $('.cardlist');
		
		cardlists.each(function () {
			var elm = $(this);
			var cardnames = elm.find('.data').html().split('|');
			console.log(cardnames);
			elm.append(makeInnerDiv(cardnames));
		});
	}
	
	run();
}