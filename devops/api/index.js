import { AstrologyService } from "./services/astrology.service.mjs";
import { CustomFortuneService } from "./services/custom-fortune.service.mjs";
import express from "express";

const app = express();
const port = 3000; // Change this to your desired port number

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});

// allow CORS
app.use(function (req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  next();
});

app.get("/", (req, res) => {
  res.send("Hello, World!");
});

// Define endpoint for getting a random astrology-based prediction
app.get("/api/astrology/random", (req, res) => {
  const astrologyService = new AstrologyService(req.query.lang);
  const prediction = astrologyService.getRandomAstrologyPrediction();
  res.json({ prediction });
});

// Define endpoint for getting a custom fortune prediction
app.get("/api/fortune/custom", (req, res) => {
  const category = req.query.category;
  const customFortuneService = new CustomFortuneService(req.query.lang);
  const prediction = customFortuneService.getCustomFortune(category);
  res.json({ prediction });
});

// Define endpoint for getting a random custom fortune prediction
app.get("/api/fortune/random", (req, res) => {
  const customFortuneService = new CustomFortuneService(req.query.lang);
  const prediction = customFortuneService.getRandomCustomFortune();
  res.json({ prediction });
});
