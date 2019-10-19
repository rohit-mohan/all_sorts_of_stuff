console.log('welcome to svg lines');

// create a container

function createContainer(parent){
    var container = document.createElement('div');
    container.style.position = 'absolute';
    container.style.width = '100%';
    container.style.height = '100%';
    container.style.padding = '0px';
    container.style.margin = '0px';
    container.style.background = 'black';

    parent.appendChild(container);

    return container;
}

function createSVG(parent){
    var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('width', '100%');
    svg.setAttribute('height', '100%');
    svg.setAttribute('background', 'lightblue');

    parent.appendChild(svg);

    return svg;
}

function createDiv(background, border, top, left, text, parent) {
    var div = document.createElement('div');
    div.style.position = 'absolute';
    div.style.background = background;
    div.style.border = border;
    div.style.top = `${top}px`;
    div.style.left = `${left}px`;
    div.innerHTML = text;
    div.style.cursor = 'pointer';
    div.style.borderRadius = '5%';
    div.style.margin = '2px';

    div.setAttribute('class', 'node');
    div.setAttribute('contenteditable', 'true');

    parent.appendChild(div);

    div.initialPosition = div.getBoundingClientRect();
    div.connectedLines = [];

    div.onDivChange = function () {
        //console.log(this.innerHTML);
        var currentPosition = this.getBoundingClientRect();
        var x = currentPosition.left + (currentPosition.width) / 2;
        var y = currentPosition.top + (currentPosition.height) / 2;
        for (var i = 0; i < this.connectedLines.length; i++){
            if (this.connectedLines[i].end == 'start') {
                this.connectedLines[i].line.setAttribute('x1', x);
                this.connectedLines[i].line.setAttribute('y1', y);
            } else {
                this.connectedLines[i].line.setAttribute('x2', x);
                this.connectedLines[i].line.setAttribute('y2', y);
            }
        }
    };

    return div;
}

function createLine(x1, y1, x2, y2, color, width, parent) {
    var line = document.createElementNS('http://www.w3.org/2000/svg','line');
    line.setAttribute('x1', x1);
    line.setAttribute('y1', y1);
    line.setAttribute('x2', x2);
    line.setAttribute('y2', y2);
    line.setAttribute('stroke', color);
    line.setAttribute('stroke-width', width);

    parent.appendChild(line);

    return line;
}

function connectDivs(startDiv, endDiv, color, width, parent){
    var startDivPosition = startDiv.getBoundingClientRect();
    var endDivPosition = endDiv.getBoundingClientRect();

    var x1 = startDivPosition.left + (startDivPosition.width / 2);
    var y1 = startDivPosition.top + (startDivPosition.height / 2);
    var x2 = endDivPosition.left + (endDivPosition.width / 2);
    var y2 = endDivPosition.top + (endDivPosition.height / 2);

    var line = createLine(x1, y1, x2, y2, color, width, parent);
    startDiv.connectedLines.push({line: line, end: 'start'});
    endDiv.connectedLines.push({line: line, end: 'end'});

    return line;
}

function makeDivDraggable(div) {
    var parent = div.parentElement;
    var offset;
    function mouseDown(event) {
        var currentPosition = this.getBoundingClientRect();
        offset = {left: event.clientX - currentPosition.left,
                      top: event.clientY - currentPosition.top};
        parent.addEventListener('mousemove', mouseMove, false);
        parent.addEventListener('mouseup', mouseUp, false);

        //console.log('mouseDown offset : ', offset, ' div : ', div.innerHTML);
    }

    function mouseMove(event) {
        var left = event.clientX - offset.left - div.initialPosition.left;
        var top = event.clientY - offset.top - div.initialPosition.top;
        div.style.transform = `translate3d(${left}px, ${top}px, 0)`;
        div.onDivChange();
    }

    function mouseUp(event) {
        parent.removeEventListener('mouseup', mouseUp, false);
        parent.removeEventListener('mousemove', mouseMove, false);

        //console.log('mouseUp div : ', div.innerHTML);
    }

    div.addEventListener('mousedown', mouseDown, false);
}

var container = createContainer(document.body);
var svg = createSVG(container);
var div1 = createDiv('rgb(236,236, 120)',
                     '2px solid rgba(136,136,136,0.5)',
                     30,
                     100,
                     'Hello!',
                     container);

var div2 = createDiv('rgb(236, 36, 120)',
                     '2px solid rgba(136,136,136,0.5)',
                     300,
                     500,
                     'World',
                     container);

var div3 = createDiv('rgb(100, 100, 200)',
                     '2px solid rgba(136,136,136,0.5)',
                     500,
                     200,
                     'Citizens',
                     container);


makeDivDraggable(div1);
makeDivDraggable(div2);
makeDivDraggable(div3);

var line12 = connectDivs(div1, div2, 'white', '2px', svg);
var line23 = connectDivs(div2, div3, 'red', '2px', svg);
