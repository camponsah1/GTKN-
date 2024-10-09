let animation = {
    revealDistance: 150,
    intitialOpacity: 0,
    transitionDelay: 0,
    transitionDuration: '2s',
    transitionProperty: 'all',
    transitionTimingFunction: 'ease'

}

let revealableContainers = document.querySelectorAll(".revealable");

function reveal() {
    for (let i=0; i < revealableContainers.length; i++) {
        let windowheight = window.innerHeight;
        let topofRevealable = revealableContainers[i].getBoundingClientRect().top;
        console.log(`Element ${i}: top = ${topofRevealable}, window height = ${windowheight}`);
        if (topofRevealable < windowheight - animation.revealDistance)
            {
                revealableContainers[i].classList.add("active");
        }
        else{
            revealableContainers[i].classList.remove("active");
        }
    }
}
window.addEventListener('scroll', reveal);

