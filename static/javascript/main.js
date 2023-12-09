let uploadInput = document.getElementById("upload-input");
uploadInput.addEventListener("change", handleUpload);
let canvas_left_position_in_image = 0, canvas_top_position_in_image = 0;

function handleUpload(event) {
    const input = event.target;
    const reader = new FileReader();
    canvasHistory = []
    currentCanvasStatePosition = -1;
    canvas_left_position_in_image = 0;
    canvas_top_position_in_image = 0;
    reader.onload = function () {
        let image = document.getElementById("uploaded-image");
        image.src = reader.result;
        image.style.display = "inline";

        image.onload = function () {
            const image_style = window.getComputedStyle(image);
            createCanvas(image_style.getPropertyValue('left'), image_style.getPropertyValue('top'));
            document.getElementById('move_button').click();
            addCanvasState();
        }
    };
    reader.readAsDataURL(input.files[0]);
}

function createCanvas(position_left, position_top) {
    let canvas = document.getElementById('sliding-window');
    const context = canvas.getContext('2d');
    canvas.style.display = '';
    context.clearRect(0, 0, canvas.width, canvas.height);
    canvas.setAttribute("class", "canvas");
    canvas.style.top = position_top;
    canvas.style.left = position_left;
}

function adjustCanvasPosition() {
    let image = document.getElementById("uploaded-image");
    let image_style = window.getComputedStyle(image);
    let imageTop = image_style.getPropertyValue('top');
    let imageLeft = image_style.getPropertyValue('left');
    let canvas = document.getElementById("sliding-window");
    if (canvas) {
        canvas.style.top = parseInt(imageTop) + canvas_top_position_in_image + 'px';
        canvas.style.left = parseInt(imageLeft) + canvas_left_position_in_image + 'px';
    }
}

window.addEventListener("resize", adjustCanvasPosition);


const canvas = document.getElementById('sliding-window');
const context = canvas.getContext('2d');
const image = document.getElementById('uploaded-image');
const thicknessSlider = document.getElementById('thicknessSlider')
let isDragging = false;
let isDrawing = false;
let isErasing = false;
let canvasLeft = 0;
let canvasTop = 0;
let canvasHistory = [];
let currentCanvasStatePosition = -1;
let thickness = 1;

function addCanvasState() {
    currentCanvasStatePosition++;
    if (currentCanvasStatePosition < canvasHistory.length)
        canvasHistory.length = currentCanvasStatePosition;

    canvasHistory.push(canvas.toDataURL());
}

const startMovingCanvas = function (event) {
    let imageRect = document.getElementById("uploaded-image").getBoundingClientRect();
    let canvasRect = canvas.getBoundingClientRect();

    canvasLeft = event.clientX - imageRect.left - canvasRect.left;
    canvasTop = event.clientY - imageRect.top - canvasRect.top;
    isDragging = true;
}

const stopMovingCanvas = function () {
    isDragging = false;
}

const moveCanvas = function (event) {
    if (isDragging) {
        let imageRect = document.getElementById("uploaded-image").getBoundingClientRect();
        let imageTop = imageRect.top;
        let imageLeft = imageRect.left;

        let newX = event.clientX - imageLeft - canvasLeft;
        let newY = event.clientY - imageTop - canvasTop;
        const maxX = imageLeft + image.clientWidth - canvas.width;
        const maxY = imageTop + image.clientHeight - canvas.height;

        if (newX < imageLeft) newX = imageLeft;
        if (newX > maxX) newX = maxX;
        if (newY < imageTop) newY = imageTop;
        if (newY > maxY) newY = maxY;

        let image_style = window.getComputedStyle(image);
        let new_canvas_left_value = parseInt(image_style.getPropertyValue('left')) + newX - imageLeft + 'px';
        let new_canvas_top_value = parseInt(image_style.getPropertyValue('top')) + newY - imageTop + 'px';
        canvas.style.left = new_canvas_left_value;
        canvas.style.top = new_canvas_top_value;
        canvas_left_position_in_image = parseInt(canvas.style.left) - parseInt(image_style.getPropertyValue('left'));
        canvas_top_position_in_image = parseInt(canvas.style.top) - parseInt(image_style.getPropertyValue('top'));
    }
}

const startDrawing = function (event) {
    isDrawing = true;
    context.beginPath();
    context.moveTo(event.offsetX, event.offsetY);
}

const stopDrawing = function (event) {
    isDrawing = false;
    if (event.type === 'mouseup')
        addCanvasState();
}

const drawInCanvas = function (event) {
    if (isDrawing) {
        context.lineTo(event.offsetX, event.offsetY);
        context.lineWidth = thickness;
        context.strokeStyle = '#000000';
        context.stroke();
    }
}

document.getElementById("move_button").addEventListener('click', function () {
    canvas.removeEventListener('mousedown', startDrawing);
    canvas.removeEventListener('mouseup', stopDrawing);
    canvas.removeEventListener('mouseout', stopDrawing);
    canvas.removeEventListener('mousemove', drawInCanvas);
    canvas.removeEventListener('mousedown', startErasing);
    canvas.removeEventListener('mouseup', stopErasing);
    canvas.removeEventListener('mouseout', stopErasing);
    canvas.removeEventListener('mousemove', eraseFromCanvas);
    canvas.classList.remove("canvas-draw");
    canvas.classList.remove("canvas-erase");

    canvas.classList.add("canvas-move");
    canvas.addEventListener('mousedown', startMovingCanvas);
    canvas.addEventListener('mouseup', stopMovingCanvas);
    canvas.addEventListener('mouseout', stopMovingCanvas);
    canvas.addEventListener('mousemove', moveCanvas);
})

document.getElementById("drawing_button").addEventListener('click', function () {
    if (image.src) {
        canvas.removeEventListener('mousedown', startMovingCanvas);
        canvas.removeEventListener('mouseup', stopMovingCanvas);
        canvas.removeEventListener('mouseout', stopMovingCanvas);
        canvas.removeEventListener('mousemove', moveCanvas);
        canvas.removeEventListener('mousedown', startErasing);
        canvas.removeEventListener('mouseup', stopErasing);
        canvas.removeEventListener('mouseout', stopErasing);
        canvas.removeEventListener('mousemove', eraseFromCanvas);
        canvas.classList.remove("canvas-move");
        canvas.classList.remove("canvas-erase");

        canvas.classList.add("canvas-draw");
        canvas.addEventListener('mousedown', startDrawing);
        canvas.addEventListener('mouseup', stopDrawing);
        canvas.addEventListener('mouseout', stopDrawing);
        canvas.addEventListener('mousemove', drawInCanvas);
    }
});


const startErasing = function (event) {
    isErasing = true;
    context.beginPath();
    context.moveTo(event.offsetX, event.offsetY);
}

const stopErasing = function (event) {
    isErasing = false;
    context.globalCompositeOperation = 'destination-over';
    if (event.type === 'mouseup')
        addCanvasState();
}

const eraseFromCanvas = function (event) {
    if (isErasing) {
        context.strokeStyle = '#000000';
        context.lineWidth = thickness;
        context.globalCompositeOperation = "destination-out";
        context.lineTo(event.offsetX, event.offsetY);
        context.stroke();
    }
}

document.getElementById('eraser_button').addEventListener('click', function () {
    if (image.src) {
        canvas.removeEventListener('mousedown', startMovingCanvas);
        canvas.removeEventListener('mouseup', stopMovingCanvas);
        canvas.removeEventListener('mouseout', stopMovingCanvas);
        canvas.removeEventListener('mousemove', moveCanvas);
        canvas.removeEventListener('mousedown', startDrawing);
        canvas.removeEventListener('mouseup', stopDrawing);
        canvas.removeEventListener('mouseout', stopDrawing);
        canvas.removeEventListener('mousemove', drawInCanvas);
        canvas.classList.remove("canvas-draw");
        canvas.classList.remove("canvas-move");

        canvas.classList.add("canvas-erase");
        canvas.addEventListener('mousedown', startErasing);
        canvas.addEventListener('mouseup', stopErasing);
        canvas.addEventListener('mouseout', stopErasing);
        canvas.addEventListener('mousemove', eraseFromCanvas);
    }
})

let undo = function () {
    if (currentCanvasStatePosition > 0) {
        currentCanvasStatePosition--;
        restoreCanvasState();
    }
}


let redo = function () {
    if (currentCanvasStatePosition < canvasHistory.length - 1) {
        currentCanvasStatePosition++;
        restoreCanvasState();
    }
};

function restoreCanvasState() {
    context.clearRect(0, 0, canvas.width, canvas.height);

    let state = canvasHistory[currentCanvasStatePosition];
    let canvasState = new Image();
    canvasState.src = state;
    canvasState.onload = function () {
        context.drawImage(canvasState, 0, 0);
    };
}

document.getElementById('undo_button').addEventListener('click', undo);
document.getElementById('redo_button').addEventListener('click', redo);

thicknessSlider.addEventListener('input', function () {
    thickness = this.value;
})

function sendImage() {
    const destinationCanvas = document.createElement('canvas');
    destinationCanvas.width = 64;
    destinationCanvas.height = 64;
    const destinationContext = destinationCanvas.getContext('2d');
    destinationContext.drawImage(canvas, 0, 0);
    destinationContext.globalCompositeOperation = "destination-over";
    destinationContext.fillStyle = "#ffffff"; // white color
    destinationContext.fillRect(0, 0, destinationCanvas.width, destinationCanvas.height);

    const image_style = window.getComputedStyle(image);
    let imageCanvas = document.createElement('canvas');
    imageCanvas.width = parseInt(image_style.getPropertyValue('width'));
    imageCanvas.height = parseInt(image_style.getPropertyValue('height'));
    const imageCanvasContext = imageCanvas.getContext('2d');
    imageCanvasContext.drawImage(image, 0, 0, parseInt(image_style.getPropertyValue('width')),
        parseInt(image_style.getPropertyValue('height')));
    let data = {
        canvas: destinationCanvas.toDataURL("image/jpg"),
        original_image: imageCanvas.toDataURL("image/jpg"),
        left: canvas_left_position_in_image,
        top: canvas_top_position_in_image
    };
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/inpaint', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(data));

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            let response = JSON.parse(xhr.responseText);
            if (xhr.status === 200) {
                image.src = 'data:image/jpg;base64,' + response.image;
                canvasHistory = []
                currentCanvasStatePosition = -1;
                canvas_left_position_in_image = 0;
                canvas_top_position_in_image = 0;
            } else {
                console.log('failed');
            }
        }
    }
}

document.getElementById("inpaint_button").addEventListener('click', sendImage);

function download_image() {
    let link = document.createElement('a');
    link.setAttribute('href', image.src);
    link.download = "inpainted_image.jpg"
    link.click()
}

document.getElementById("download_button").addEventListener('click', download_image);
