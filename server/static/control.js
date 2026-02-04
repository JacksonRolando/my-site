const radiansRadiusToPos = (radians, remRadius) => {
    let degreeRadius = remRadius * parseFloat(getComputedStyle(document.documentElement).fontSize);
    let x = Math.round(degreeRadius * Math.cos(radians))
    let y = Math.round(degreeRadius * Math.sin(radians))
    return { x, y }
}

const circleSplit = (numElementsToAdd, offset = 0) => {
    let radiansList = []
    let increment = 2 * Math.PI / numElementsToAdd

    for (let i = 0; i < numElementsToAdd; i++) {
        radiansList.push(offset + increment * i)
    }

    return radiansList
}

const fanStack = (stackElementId, offsetRadians = 0, remRadius = 10) => {
    const children = document.getElementById(stackElementId).children

    const radiansList = circleSplit(children.length - 1, offsetRadians)
    const posList = []

    radiansList.forEach(radian => {
        posList.push(radiansRadiusToPos(radian, remRadius))
    });

    for (let i = 1; i < children.length; i++) {
        let child = children[i].children[0]
        child.style.translate = `calc(-50% - ${posList[i - 1].x}px) ${posList[i - 1].y}px`
        child.classList.add('stack-card-under-shown')
    }

    window.addEventListener('click', function (e) {
        if (!document.getElementById(stackElementId).contains(e.target)) {
            for (let i = 1; i < children.length; i++) {
                let child = children[i].children[0]
                child.classList.remove('stack-card-under-shown')
            }
        }
    });

}