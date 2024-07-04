// App.js

import { useEffect, useRef, useState } from "react";
import Button from "@mui/material/Button";
import "./App.css";
import { Typography } from "@mui/material";

function App() {
  const canvasRef = useRef(null);
  const ctxRef = useRef(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const lineWidth = 15;
  const lineColor = "black";
  const lineOpacity = 2;
  const [drawStack, setDrawStack] = useState([]);
  const [answer, setAnswer] = useState("ANSWER HERE");

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
    ctx.globalAlpha = lineOpacity;
    ctx.strokeStyle = lineColor;
    ctx.lineWidth = lineWidth;
    ctxRef.current = ctx;
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
  }, [lineColor, lineOpacity, lineWidth]);

  const clearCanvas = () => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    setDrawStack([]);
  };

  // Function for starting the drawing
  const startDrawing = (e) => {
    ctxRef.current.beginPath();
    ctxRef.current.moveTo(e.nativeEvent.offsetX, e.nativeEvent.offsetY);
    setIsDrawing(true);
  };

  // Function for ending the drawing
  const endDrawing = () => {
    setDrawStack([...drawStack, ctxRef.current.getImageData(0, 0, 1280, 720)]);
    ctxRef.current.closePath();
    setIsDrawing(false);
  };

  const draw = (e) => {
    if (!isDrawing) {
      return;
    }
    ctxRef.current.lineTo(e.nativeEvent.offsetX, e.nativeEvent.offsetY);
    ctxRef.current.stroke();
  };

  const handleSubmit = () => {
    const canvas = canvasRef.current;
    const dataURL = canvas.toDataURL("image/png");

    fetch("http://localhost:5000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        data: dataURL,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        setAnswer(data.prediction[0] + " --> " + data.prediction[1]);
      });
  };

  return (
    <div className="App">
      <Typography variant="h4" style={{ marginTop: 20 }}>
        {answer}
      </Typography>
      <div className="draw-area">
        <canvas
          onMouseDown={startDrawing}
          onMouseUp={endDrawing}
          onMouseMove={draw}
          ref={canvasRef}
          width={`1280px`}
          height={`720px`}
        />
        <Button
          style={{ marginTop: 10 }}
          variant="outlined"
          onClick={handleSubmit}
        >
          Submit
        </Button>
        <Button
          style={{ marginTop: 10, marginLeft: 30 }}
          variant="outlined"
          onClick={clearCanvas}
        >
          Clear
        </Button>
      </div>
    </div>
  );
}

export default App;
