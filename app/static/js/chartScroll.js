// function scrollMobile() {
//    alert("Hello World")
// }

function scrollMobile() {
	console.log("ran scroll mobile")

	let value = 500;
	let windowWidth = (window.innerWidth > 0) ? window.innerWidth : screen.width;
    //let offset = (windowWidth <700) ? value : 0;
    let offset = value
    var scrolledAmount = 0

    window.scrollTo(0,offset)

    // scrollInterval = setInterval(function(){
    //     if ( window.scrollY < offset ) {
    //         window.scrollBy( 0, 10 );
    //         console.log("scrolling")

    //         scrolledAmount++
    //     }
    //     else clearInterval(scrollInterval); 
    // },5);

}

